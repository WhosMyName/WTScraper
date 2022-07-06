""" Class description of a ground vehicle from WarThunder
"""

from enum import Enum
from armament import Armament
from typing import Dict, Tuple, List

class VehicleClass(Enum):
    DEFAULT = 1
    LIGHT = 2
    MEDIUM = 3
    HEAVY = 4
    SPG = 5
    SPAA = 6

class Tank():
    """Class that represents a WarThunder Ground Vehicle
    """
    name: str = "Generic Ground Vehicle"
    vehicle_class: VehicleClass = VehicleClass.DEFAULT
    armaments: List[Armament] = []
    armour: Tuple[int, int, int] = (-1, -1, -1)
    armour_hull: Tuple[int, int, int] = (-1, -1, -1)
    armour_turret: Tuple[int, int, int] = (-1, -1, -1)
    crew: int = -1
    visibility: int = -1
    weight: float = -1.0
    engine_power: Dict = {"RB": 0, "AB": 0}
    max_speed_forward: Dict = {"RB": 0, "AB": 0, "SB": 0}
    max_speed_reverse: Dict = {"RB": 0, "AB": 0, "SB": 0}
    gears: Dict = {"Forward": 0, "Back": 0}
    power_to_weight: Dict = {"RB": 0, "AB": 0}
    rank: int = -1
    battle_rating: Dict = {"RB": 0, "AB": 0, "SB": 0}
    is_amphibious:bool = False
    # Mods
    # Utility
    smokes: bool = False
    ess: bool = False
    artillery: bool = False
    dozer_blade: bool = False
    scouting: bool = False
    # Visuals
    night_vision: bool = False
    thermal_vision: bool = False
    # Rangefinding
    rangefinder: bool = False
    laser_rangefinder: bool = False
    laser_warning_rangefinder: bool = False


    def __init__(self, name: str):
        """
        Parameters
        ----------
        name : str
            Ground Vehicle Name
        """
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} with Armaments [{' || '.join(armament.__str__() for armament in self.armaments)}]"