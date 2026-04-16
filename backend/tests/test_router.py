import math
from src.router import calculate_distance, optimize_route

MILL = {"id": "MILL-01", "name": "Feed Mill", "x_coord": 0.0, "y_coord": 0.0}

FARM_A = {"id": "F-001", "name": "Farm A", "x_coord": 3.0, "y_coord": 4.0}   # distance 5
FARM_B = {"id": "F-002", "name": "Farm B", "x_coord": 0.0, "y_coord": 10.0}  # distance 10 from mill


def test_calculate_distance_known_values():
    dist = calculate_distance({"x_coord": 0.0, "y_coord": 0.0}, {"x_coord": 3.0, "y_coord": 4.0})
    assert dist == 5.0


def test_calculate_distance_same_point():
    dist = calculate_distance({"x_coord": 5.0, "y_coord": 5.0}, {"x_coord": 5.0, "y_coord": 5.0})
    assert dist == 0.0


def test_optimize_route_empty_list():
    result = optimize_route(MILL, [])
    assert result["route"] == []
    assert result["total_distance"] == 0.0


def test_optimize_route_single_farm():
    result = optimize_route(MILL, [FARM_A])
    steps = result["route_steps"]
    assert len(steps) == 2  # Farm A + return to base
    assert steps[0]["farm_id"] == "F-001"
    assert steps[1]["farm_name"] == "Return to Base"


def test_optimize_route_returns_all_farms():
    result = optimize_route(MILL, [FARM_A, FARM_B])
    # 2 farm stops + 1 return = 3 steps
    assert len(result["route_steps"]) == 3


def test_optimize_route_nearest_neighbor_order():
    # Farm A is closer to mill (dist=5), Farm B is farther (dist=10)
    result = optimize_route(MILL, [FARM_B, FARM_A])
    steps = result["route_steps"]
    assert steps[0]["farm_id"] == "F-001"  # Nearest visited first
    assert steps[1]["farm_id"] == "F-002"


def test_optimize_route_total_distance_positive():
    result = optimize_route(MILL, [FARM_A, FARM_B])
    assert result["total_route_distance"] > 0


def test_optimize_route_total_distance_rounded():
    result = optimize_route(MILL, [FARM_A, FARM_B])
    # Result should be rounded to 2 decimal places
    assert result["total_route_distance"] == round(result["total_route_distance"], 2)
