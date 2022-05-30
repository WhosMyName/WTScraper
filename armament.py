from ammunition import Ammunition

class Armament():
    is_secondary: bool
    ammo_types: List[Ammunition]
    diameter: float 
    capacity: int
    fire_rate: int
    vertical_guidance: Dict[str, int] = {"positive": 0, "negative": 0}
    belt_capacity: int
    reload_time: float
    fire_while_moving: int
