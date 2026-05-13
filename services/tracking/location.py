"""
Real-time location service with Kalman filtering for GPS noise reduction.
"""
import time
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional


@dataclass
class Location:
    lat: float
    lng: float
    heading: float
    speed_kmh: float
    timestamp: float = field(default_factory=time.time)


class KalmanFilter1D:
    """One-dimensional Kalman filter for smoothing scalar GPS noise."""
    def __init__(self, process_variance: float = 1e-5, measurement_variance: float = 1e-2):
        self.q = process_variance
        self.r = measurement_variance
        self.x = 0.0
        self.p = 1.0

    def update(self, z: float) -> float:
        self.p += self.q
        k = self.p / (self.p + self.r)
        self.x += k * (z - self.x)
        self.p *= (1 - k)
        return self.x


class LocationTracker:
    def __init__(self):
        self._locations: dict = {}
        self._filters: dict = defaultdict(lambda: (KalmanFilter1D(), KalmanFilter1D()))

    def update(self, driver_id: str, raw_lat: float, raw_lng: float,
               heading: float, speed_kmh: float) -> Location:
        kf_lat, kf_lng = self._filters[driver_id]
        loc = Location(kf_lat.update(raw_lat), kf_lng.update(raw_lng), heading, speed_kmh)
        self._locations[driver_id] = loc
        return loc

    def get(self, driver_id: str) -> Optional[Location]:
        return self._locations.get(driver_id)


tracker = LocationTracker()
