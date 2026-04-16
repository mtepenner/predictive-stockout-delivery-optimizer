from src.predictor import analyze_inventory

SAMPLE_FARMS = [
    {"id": "F-001", "name": "Test Farm A", "x_coord": 10.0, "y_coord": 10.0,
     "capacity_tons": 20.0, "current_tons": 2.0, "daily_burn_rate": 1.0},  # 2 days → critical
    {"id": "F-002", "name": "Test Farm B", "x_coord": 5.0, "y_coord": 5.0,
     "capacity_tons": 30.0, "current_tons": 20.0, "daily_burn_rate": 2.0},  # 10 days → ok
    {"id": "F-003", "name": "Test Farm C", "x_coord": 0.0, "y_coord": 0.0,
     "capacity_tons": 10.0, "current_tons": 3.0, "daily_burn_rate": 1.0},  # 3 days → critical at threshold=3
    {"id": "F-004", "name": "Test Farm D", "x_coord": 0.0, "y_coord": 0.0,
     "capacity_tons": 10.0, "current_tons": 0.0, "daily_burn_rate": 0.0},  # zero burn rate
]


def test_critical_farm_flagged():
    status = analyze_inventory(SAMPLE_FARMS, critical_days_threshold=3)
    farm_a = next(s for s in status if s["farm_id"] == "F-001")
    assert farm_a["needs_delivery"] is True


def test_healthy_farm_not_flagged():
    status = analyze_inventory(SAMPLE_FARMS, critical_days_threshold=3)
    farm_b = next(s for s in status if s["farm_id"] == "F-002")
    assert farm_b["needs_delivery"] is False


def test_farm_exactly_at_threshold_is_critical():
    status = analyze_inventory(SAMPLE_FARMS, critical_days_threshold=3)
    farm_c = next(s for s in status if s["farm_id"] == "F-003")
    assert farm_c["days_remaining"] == 3.0
    assert farm_c["needs_delivery"] is True


def test_days_remaining_calculation():
    status = analyze_inventory(SAMPLE_FARMS, critical_days_threshold=3)
    farm_a = next(s for s in status if s["farm_id"] == "F-001")
    assert farm_a["days_remaining"] == 2.0


def test_fill_percentage_calculation():
    status = analyze_inventory(SAMPLE_FARMS, critical_days_threshold=3)
    farm_a = next(s for s in status if s["farm_id"] == "F-001")
    assert farm_a["fill_percentage"] == 10.0  # 2/20 * 100


def test_zero_burn_rate_returns_zero_days():
    status = analyze_inventory(SAMPLE_FARMS, critical_days_threshold=3)
    farm_d = next(s for s in status if s["farm_id"] == "F-004")
    assert farm_d["days_remaining"] == 0


def test_all_farms_returned():
    status = analyze_inventory(SAMPLE_FARMS, critical_days_threshold=3)
    assert len(status) == len(SAMPLE_FARMS)


def test_custom_threshold():
    status = analyze_inventory(SAMPLE_FARMS, critical_days_threshold=1)
    farm_a = next(s for s in status if s["farm_id"] == "F-001")
    farm_c = next(s for s in status if s["farm_id"] == "F-003")
    assert farm_a["needs_delivery"] is False  # 2 days > threshold 1, so NOT critical
    assert farm_c["needs_delivery"] is False  # 3 days > threshold 1, so NOT critical
