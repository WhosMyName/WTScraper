"""Class description of a ground vehicle armament ammunition from WarThunder
"""

from typing import Dict


class Ammunition():
    """Class that represents a firable round from WarThunder
    """

    def __init__(self, name: str, ammo_type: str, pen_at_distance: Dict[int, int]) -> None:
        """_summary_

        Parameters
        ----------
        name : str
            name of the round
        ammo_type : str
            type of the round (AP, HE, APDS, HESH, ...)
        pen_at_distance : Dict[int, int]
            penetration of the round at different distances
        """
        self.name: str = name
        self.ammo_type: str = ammo_type
        self.pen_at_distance: Dict[str, int] = pen_at_distance # {"10": -1, "100": -1, "500": -1, "1000": -1, "1500": -1, "2000": -1}
        self.ricochet: Dict[str, int] = {"0%": -1, "50%": -1, "100%": -1}
        self.velocity: int = -1
        self.explosive_mass: int
        self.projectile_mass: float = -1.0
        self.fuse_delay: float
        self.fuse_sensitivity: float
        self.range: int

    def __str__(self) -> str:
        """returns the summary of a shell

        Returns
        -------
        str
            shell name and shell type
        """
        return f"{self.name}: {self.ammo_type}"