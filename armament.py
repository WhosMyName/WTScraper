"""Class description of a ground vehicle armament from WarThunder
"""

from enum import Enum
from ammunition import Ammunition
from typing import List, Dict

#class Stbilizer(Enum):

class Stabilizer(Enum):
    NONE = 1
    VERTICAL = 2
    SHOULDER = 3
    TWOPLANE = 4


class Armament():
    name: str
    ammo_types: List[Ammunition] = []
    vertical_guidance: Dict[str, int] = {"positive": 0, "negative": 0}
    reload_time: Dict[str, float] = {"basic": 0.0, "aces": 0.0}
    diameter: float = -1.0
    fire_rate: int = -1
    fire_while_moving: bool = False # check how this is handled, it might be a max_firing_speed!! # it is!
    first_stowage: int = -1
    capacity: int = -1
    belt_capacity: int = -1
    stabilizer: Stabilizer = Stabilizer.NONE
    autoloader: bool = False

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} with Rounds: [{' | '.join(ammo.__str__() for ammo in self.ammo_types) or 'Default'}]"
