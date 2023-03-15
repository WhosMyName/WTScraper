"""Class description of a ground vehicle armament from WarThunder
"""

from enum import Enum
from ammunition import Ammunition
from typing import List, Dict

class Stabilizer(Enum):
    """Enum Class that represents a Armament Stabilizer
    """
    NONE = 1
    VERTICAL = 2
    SHOULDER = 3
    TWOPLANE = 4


class Armament():
    """Class that represents a WarThunder Ground Vehicle Armament (Waepon)
    """

    def __init__(self, name: str) -> None:
        """ init

        Parameters
        ----------
        name : str
            Name of the armament
        """
        self.name: str = name
        self.ammo_types: List[Ammunition] = []
        self.vertical_guidance: Dict[str, int] = {"positive": 0, "negative": 0}
        self.reload_time: Dict[str, float] = {"stock": 0.0, "full": 0.0, "expert": 0.0, "aces": 0.0}
        self.rotation_speed_arcade: Dict[str, float] = {"stock": 0.0, "upgraded": 0.0, "full": 0.0, "expert": 0.0, "aces": 0.0}
        self.rotation_speed_realistic: Dict[str, float] = {"stock": 0.0, "upgraded": 0.0, "full": 0.0, "expert": 0.0, "aces": 0.0}
        self.diameter: float = -1.0
        self.fire_rate: int = -1
        self.fire_while_moving: bool = False # check how this is handled, it might be a max_firing_speed!! # it is!
        self.first_stowage: int = -1
        self.capacity: int = -1
        self.belt_capacity: int = -1
        self.stabilizer: Stabilizer = Stabilizer.NONE
        self.autoloader: bool = False

    def __str__(self) -> str:
        """returns a summary of an armament

        Returns
        -------
        str
            armament name and a list of the usable rounds
        """
        return f"{self.name} with Rounds: [{' | '.join(ammo.__str__() for ammo in self.ammo_types) or 'Default'}]"
