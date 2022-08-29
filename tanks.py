""" Class description of a ground vehicle from WarThunder
"""

from enum import Enum
from armament import Armament
from typing import Dict, Tuple, List

class VehicleClass(Enum):
    """ an enum that represents a vehicles designation
    """
    DEFAULT = 1
    LIGHT = 2
    MEDIUM = 3
    HEAVY = 4
    TANK_DESTROYER = 5
    SPAA = 6

class Tank():
    """Class that represents a WarThunder Ground Vehicle
    """

    def __init__(self, name: str):
        """
        Parameters
        ----------
        name : str
            Ground Vehicle Name
        """
        # General
        self.name: str = name
        self.vehicle_class: VehicleClass = VehicleClass.DEFAULT
        self.nation: str = ""
        self.is_premium: bool = False
        self.is_squadron: bool = False
        self.rank: int = -1
        self.battle_rating: Dict[str, float] = {"Arcade": 0.0, "Realistic": 0.0, "Simulator": 0.0}
        self.armaments: List[Armament] = []
        self.cost: int = -1
        self.research: int = -1
        self.repair_cost_stock: Dict[str, int] = {"Arcade": -1, "Realistic": -1, "Simulator": -1}
        self.repair_cost_upgraded: Dict[str, int] = {"Arcade": -1, "Realistic": -1, "Simulator": -1}
        self.total_cost_modifications_sl: int = -1
        self.total_cost_modifications_rp: int = -1
        self.crew_training: int = -1
        self.talisman_cost: int = -1
        self.rewards_sl: Dict[str, int] = {"Arcade": -1, "Realistic": -1, "Simulator": -1}
        self.rewards_rp: Dict[str, int] = {"Arcade": -1, "Realistic": -1, "Simulator": -1}
        # Armour
        self.armour_hull: Dict[str, int] = {"front": -1, "side": -1, "back": -1}
        self.armour_turret: Dict[str, int] = {"front": -1, "side": -1, "back": -1}
        # Stuff
        self.crew: int = -1
        self.visibility: int = -1
        self.weight: float = -1.0
        # Movement and Engine
        self.gears: Dict[str, int] = {"Forward": 0, "Back": 0}
        self.max_speed_forward: Dict[str, int] = {"Realistic": 0, "Arcade": 0}
        self.max_speed_reverse: Dict[str, int] = {"Realistic": 0, "Arcade": 0}
        self.power_to_weight_stock: Dict[str, float] = {"Realistic": 0, "Arcade": 0}
        self.power_to_weight_upgraded: Dict[str, float] = {"Realistic": 0, "Arcade": 0}
        self.engine_power_stock: Dict[str, int] = {"Realistic": 0, "Arcade": 0}
        self.engine_power_upgraded: Dict[str, int] = {"Realistic": 0, "Arcade": 0}
        # Features
        self.era: bool = False
        self.is_amphibious:bool = False
        self.reverse_gearbox: bool = False
        self.controlled_suspension: bool = False
        # Mods
        # Utility
        self.smokes: bool = False
        self.ess: bool = False
        self.artillery: bool = False
        self.dozer_blade: bool = False
        self.scouting: bool = False
        # Visuals
        self.night_vision: bool = False
        self.thermal_vision: bool = False
        # Rangefinding
        self.rangefinder: bool = False
        self.laser_rangefinder: bool = False
        self.laser_warning_rangefinder: bool = False

    def __str__(self) -> str:
        """returns a summary of a ground vehicle

        Returns
        -------
        str
            vehicle name and a list of it's armaments
        """
        return f"{self.name} with Armaments [{' || '.join(armament.__str__() for armament in self.armaments)}]"