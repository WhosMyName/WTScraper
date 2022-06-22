from ammunition import Ammunition
from typing import List, Dict

class Armament():
    name: str
    is_secondary: bool
    ammo_types: List[Ammunition] = []
    vertical_guidance: Dict[str, int] = {"positive": 0, "negative": 0}
    reload_time: Dict[str, float] = {"basic": 0.0, "aces": 0.0}
    diameter: float
    fire_rate: int
    fire_while_moving: int
    first_stowage: int
    capacity: int
    belt_capacity: int

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} with Rounds: [{' | '.join(ammo.__str__() for ammo in self.ammo_types) or 'Default'}]"
