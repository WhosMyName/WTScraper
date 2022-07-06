"""Class description of a ground vehicle armament ammunition from WarThunder
"""

from typing import Dict


class Ammunition():
    name: str
    ammo_type: str
    pen_at_distance: Dict[str, int] = {"10": -1, "100": -1, "500": -1, "1000": -1, "1500": -1, "2000": -1}
    ricochet: Dict[str, int] = {"0%": -1, "50%": -1, "100%": -1}
    explosive_mass: float = -1.0
    velocity: int
    projectile_mass: float
    fuse_delay: float
    fuse_sensitivity: float

    def __init__(self, name: str, ammo_type: str, pen_at_distance: Dict[int, int]) -> None:
        self.name = name
        self.ammo_type = ammo_type
        self.pen_at_distance = pen_at_distance
    def __str__(self) -> str:
        return f"{self.name}: {self.ammo_type}"