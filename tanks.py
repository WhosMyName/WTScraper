from armament import Armament

lass Tank():
    name: str
    armaments: List[Armament]
    armour_hull: Tuple[int, int, int]
    armour_turret: Tuple[int, int, int]
    crew: int
    visibility: int
    smokes: int
    ess: bool
    stabilizer: int # 0 planes 1 plane  2 plane
    weight: float
    engine_power: Dict = {"RB": 0, "AB": 0}
    max_speed_forward: Dict = {"RB": 0, "AB": 0, "SB": 0}
    max_speed_reverse: Dict = {"RB": 0, "AB": 0, "SB": 0}
    gears: Dict = {"Forward": 0, "Back": 0}
    power_to_weight: Dict = {"RB": 0, "AB": 0}
    night_vision: bool
    thermal_vision: bool


