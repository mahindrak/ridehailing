"""
Surge pricing engine — dynamic fare multiplier based on zone demand.
"""
from dataclasses import dataclass


@dataclass
class DemandSignal:
    active_requests: int
    available_drivers: int
    weather_factor: float = 1.0   # 1.0 clear, 1.5 rain, 2.0 storm
    event_factor:   float = 1.0   # 1.0 normal, 1.5 stadium, 2.0 concert

    @property
    def supply_demand_ratio(self) -> float:
        if self.available_drivers == 0:
            return float("inf")
        return self.active_requests / self.available_drivers


def calculate_surge(signal: DemandSignal, cap: float = 3.0) -> float:
    """Returns surge multiplier rounded to nearest 0.1, capped at cap."""
    sdr = signal.supply_demand_ratio
    if   sdr < 1.2: base = 1.0
    elif sdr < 1.5: base = 1.2
    elif sdr < 2.0: base = 1.5
    elif sdr < 3.0: base = 2.0
    else:           base = 2.5
    raw     = base * signal.weather_factor * signal.event_factor
    rounded = round(raw * 10) / 10
    return min(rounded, cap)


def driver_bonus_eligible(multiplier: float) -> bool:
    return multiplier >= 1.5
