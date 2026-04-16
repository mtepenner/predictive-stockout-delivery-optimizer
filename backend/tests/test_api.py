from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_returns_active_status():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_inventory_status_returns_data():
    response = client.get("/api/inventory/status")
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) > 0


def test_inventory_status_record_shape():
    response = client.get("/api/inventory/status")
    record = response.json()["data"][0]
    for key in ("farm_id", "farm_name", "current_tons", "capacity_tons",
                "fill_percentage", "days_remaining", "needs_delivery"):
        assert key in record


def test_inventory_status_custom_threshold():
    response = client.get("/api/inventory/status?critical_threshold=100")
    assert response.status_code == 200
    data = response.json()["data"]
    # With a very high threshold all farms should be critical
    assert all(farm["needs_delivery"] for farm in data)


def test_daily_route_returns_logistics():
    response = client.get("/api/logistics/daily-route")
    assert response.status_code == 200
    body = response.json()
    assert "logistics" in body
    assert "deliveries_scheduled" in body
    assert "truck_id" in body


def test_daily_route_logistics_shape():
    response = client.get("/api/logistics/daily-route")
    logistics = response.json()["logistics"]
    assert "route_steps" in logistics
    assert "total_route_distance" in logistics


def test_daily_route_deliveries_count_matches_steps():
    response = client.get("/api/logistics/daily-route")
    body = response.json()
    scheduled = body["deliveries_scheduled"]
    steps = body["logistics"]["route_steps"]
    # Steps include farm stops + return to base
    assert len(steps) == scheduled + 1 or (scheduled == 0 and len(steps) == 0)
