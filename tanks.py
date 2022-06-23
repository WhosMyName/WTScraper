""" Class description of a ground vehicle from WarThunder
"""

from armament import Armament
from typing import Dict, Tuple, List

class Tank():
    """Class that represents a WarThunder Ground Vehicle
    """
    name: str
    armaments: List[Armament]
    armour_hull: Tuple[int, int, int]
    armour_turret: Tuple[int, int, int]
    crew: int
    visibility: int
    #stabilizer: int # 0 planes 1 plane  2 plane
    weight: float
    engine_power: Dict = {"RB": 0, "AB": 0}
    max_speed_forward: Dict = {"RB": 0, "AB": 0, "SB": 0}
    max_speed_reverse: Dict = {"RB": 0, "AB": 0, "SB": 0}
    gears: Dict = {"Forward": 0, "Back": 0}
    power_to_weight: Dict = {"RB": 0, "AB": 0}
    rank: int
    battle_rating: float
    is_amphibious:bool
    # Mods
    # Utility
    smokes: int
    ess: bool
    artillery: bool
    dozer_blade: bool
    # Visuals
    night_vision: bool
    thermal_vision: bool
    # Rangefinding
    rangefinder: bool
    laser_rangefinder: bool
    laser_warning_rangefinder: bool

    def __init__(self, name: str):
        """
        Parameters
        ----------
        name : str
            Ground Vehicle Name
        """
        self.name = name
        self.armaments: List[Armament] = []
        self.armour_hull: Tuple[int, int, int] = ()
        self.armour_turret: Tuple[int, int, int] = ()
        self.crew: int = -1
        self.visibility: int = -1
        self.smokes: int = -1
        self.ess: bool = False
        self.stabilizer: int = -1 # 0 planes 1 plane  2 plane
        self.weight: float = -100.0
        self.engine_power: Dict = {"RB": 0, "AB": 0}
        self.max_speed_forward: Dict = {"RB": 0, "AB": 0, "SB": 0}
        self.max_speed_reverse: Dict = {"RB": 0, "AB": 0, "SB": 0}
        self.gears: Dict = {"Forward": 0, "Back": 0}
        self.power_to_weight: Dict = {"RB": 0, "AB": 0}
        self.night_vision: bool = False
        self.thermal_vision: bool = False


