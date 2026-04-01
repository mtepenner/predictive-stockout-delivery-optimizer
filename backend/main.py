from fastapi import FastAPI
from pydantic import BaseModel
from src.mock_data import FARMS, FEED_MILL
from src.predictor import analyze_inventory
from src.router import optimize_route

app = FastAPI(title="Predictive Routing API")

@app.get("/")
def read_root():
    return {"status": "active", "service": "Predictive Stockout & Delivery Optimizer"}

@app.get("/api/inventory/status")
def get_inventory_status(critical_threshold: int = 3):
    """
    Returns the calculated inventory status for all connected farms.
    """
    status = analyze_inventory(FARMS, critical_threshold)
    return {"data": status}

@app.get("/api/logistics/daily-route")
def get_optimized_route(critical_threshold: int = 3):
    """
    Identifies farms needing delivery and calculates the most efficient truck route.
    """
    # 1. Predict who needs feed
    status = analyze_inventory(FARMS, critical_threshold)
    critical_farm_ids = [farm["farm_id"] for farm in status if farm["needs_delivery"]]
    
    # 2. Extract the full data objects for those critical farms
    farms_to_visit = [farm for farm in FARMS if farm["id"] in critical_farm_ids]
    
    # 3. Calculate the route
    route_plan = optimize_route(FEED_MILL, farms_to_visit)
    
    return {
        "date": "2026-04-01", # Mock current date
        "truck_id": "TRK-09",
        "deliveries_scheduled": len(farms_to_visit),
        "logistics": route_plan
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
