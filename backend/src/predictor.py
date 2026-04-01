def analyze_inventory(farms, critical_days_threshold=3):
    """
    Calculates run-out dates and flags farms needing immediate delivery.
    """
    inventory_status = []
    
    for farm in farms:
        # Prevent division by zero if a farm is empty
        days_remaining = farm["current_tons"] / farm["daily_burn_rate"] if farm["daily_burn_rate"] > 0 else 0
        
        is_critical = days_remaining <= critical_days_threshold
        
        inventory_status.append({
            "farm_id": farm["id"],
            "farm_name": farm["name"],
            "current_tons": farm["current_tons"],
            "capacity_tons": farm["capacity_tons"],
            "fill_percentage": round((farm["current_tons"] / farm["capacity_tons"]) * 100, 1),
            "days_remaining": round(days_remaining, 1),
            "needs_delivery": is_critical
        })
        
    return inventory_status
