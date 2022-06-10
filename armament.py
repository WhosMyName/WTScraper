from ammunition import Ammunition
from typing import List, Dict

class Armament():
    is_secondary: bool
    ammo_types: List[Ammunition]
    diameter: float 
    capacity: int
    fire_rate: int
    vertical_guidance: Dict[str, int] = {"positive": 0, "negative": 0}
    belt_capacity: int
    reload_time: Dict[str, float] = {"basic": 0.0, "aces": 0.0}
    fire_while_moving: int
    first_stowage: int

    def __init__(self, name: str) -> None:
        self.name = name
