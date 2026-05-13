"""
Dispatch engine — assigns nearest available driver to ride request.
"""
import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class Driver:
    id: str
    lat: float
    lng: float
    rating: float
    vehicle_type: str
    is_available: bool = True


@dataclass
class RideRequest:
    id: str
    rider_id: str
    origin_lat: float
    origin_lng: float
    vehicle_type: str


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Returns distance in km between two GPS coordinates."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlng / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def score_driver(driver: Driver, request: RideRequest, demand_factor: float = 1.0) -> float:
    dist = haversine(driver.lat, driver.lng, request.origin_lat, request.origin_lng)
    if dist > 5.0:
        return -1
    proximity_score = max(0, 1 - dist / 5.0) * 60
    rating_score    = (driver.rating / 5.0) * 30
    demand_score    = min(demand_factor, 2.0) * 10
    return proximity_score + rating_score + demand_score


def dispatch(request: RideRequest, drivers: list, demand_factor: float = 1.0) -> Optional[Driver]:
    eligible = [d for d in drivers if d.is_available and d.vehicle_type == request.vehicle_type]
    if not eligible:
        return None
    scored = sorted(
        [(score_driver(d, request, demand_factor), d) for d in eligible],
        key=lambda x: x[0], reverse=True
    )
    best_score, best_driver = scored[0]
    return best_driver if best_score > 0 else None
