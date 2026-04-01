import math

def calculate_distance(p1, p2):
    """Calculates straight-line Euclidean distance between two X/Y points."""
    return math.sqrt((p1['x_coord'] - p2['x_coord'])**2 + (p1['y_coord'] - p2['y_coord'])**2)

def optimize_route(start_point, locations_to_visit):
    """
    Creates an optimized delivery route using the Nearest Neighbor algorithm.
    """
    if not locations_to_visit:
        return {"route": [], "total_distance": 0.0}

    unvisited = locations_to_visit.copy()
    current_location = start_point
    optimized_route = []
    total_distance = 0.0

    while unvisited:
        # Find the closest unvisited farm to our current location
        closest_farm = min(unvisited, key=lambda farm: calculate_distance(current_location, farm))
        
        # Add distance to total
        dist = calculate_distance(current_location, closest_farm)
        total_distance += dist
        
        # Add to route and move our current location
        optimized_route.append({
            "farm_id": closest_farm["id"],
            "farm_name": closest_farm["name"],
            "distance_from_previous": round(dist, 2)
        })
        
        current_location = closest_farm
        unvisited.remove(closest_farm)

    # Add the return trip back to the Feed Mill
    return_dist = calculate_distance(current_location, start_point)
    total_distance += return_dist
    optimized_route.append({
        "farm_id": start_point["id"],
        "farm_name": "Return to Base",
        "distance_from_previous": round(return_dist, 2)
    })

    return {
        "route_steps": optimized_route,
        "total_route_distance": round(total_distance, 2)
    }
