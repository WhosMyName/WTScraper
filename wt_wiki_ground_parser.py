"""Parsing of Ground Vehicles using data provided by the WarThunder Wiki
"""

from bs4 import BeautifulSoup, SoupStrainer, Tag
from ammunition import Ammunition
from armament import Armament, Stabilizer
from tanks import Tank, VehicleClass
from typing import Dict, List
from html_table_parser import HTMLTableParser


def parse_ground_vehicle(response_content: str) -> Tank:
    """parses the wiki entry of a ground vehicle

    Parameters
    ----------
    response_content : str
        scraped but unparsed html of a ground vehicles wiki entry


    Returns
    -------
    Tank
        a fully parsed Ground Vehicle
    """

    # TODO:
    # Radar
    # APS ?
    # Composite armour

    soup = BeautifulSoup(response_content, "html.parser", parse_only=SoupStrainer(class_="mw-parser-output"))

    # General Tank Parsing (Name, VehicleClass, Premium, Squadron)
    parsed_tank = Tank(name=soup.find(class_="general_info_name").text.strip())
    parse_vehicle_general_info(tank=parsed_tank, soup=soup)
    parse_vehicle_cost(tank=parsed_tank, soup=soup)
    parse_vehicle_specs(tank=parsed_tank, soup=soup)
    parse_vehicle_armaments(tank=parsed_tank, soup=soup)
    parse_vehicles_fetures(tank=parsed_tank, soup=soup)
    parse_vehicle_modification_features(tank=parsed_tank, soup=soup)

    print(parsed_tank.__str__())
    print(parsed_tank.__dict__)

def parse_vehicle_general_info(tank: Tank, soup: BeautifulSoup) -> None:
    """parses an vehilces general info
    Rank
    BattleRating
    VehicleClass
    Nation

    Parameters
    ----------
    tank : Tank
        the updating ground vehicle
    soup : BeautifulSoup
        wiki data on the specific ground vehicle
    """

    tank.is_squadron = True if soup.find(class_="squadron") else False
    tank.is_premium = True if soup.find(class_="premium") else False
    if tank.is_squadron:
        soup.find(class_="squadron").extract()
    if tank.is_premium:
        soup.find(class_="premium").extract()
    vehicle_class = soup.find(class_="general_info_class").find("a").text.strip() # checking if the vehicle is of a certiain class and/or premium/squadron
    if vehicle_class == "Light tank":
        tank.vehicle_class = VehicleClass.LIGHT
    elif vehicle_class == "Medium tank":
        tank.vehicle_class = VehicleClass.MEDIUM
    elif vehicle_class == "Heavy tank":
        tank.vehicle_class = VehicleClass.HEAVY
    elif vehicle_class == "SPAA":
        tank.vehicle_class = VehicleClass.SPAA
    elif vehicle_class == "Tank destroyer":
        tank.vehicle_class = VehicleClass.TANK_DESTROYER
    else:
        print(f"{tank.name}: {vehicle_class}")

    # Battle Rating, Rank, Nation
    tank.nation = soup.find(class_="general_info_nation").find_all("a")[-1].text.strip()
    text_rank = soup.find(class_="general_info_rank").a.text.strip().split(" ")[0] # "V Rank"
    if text_rank == "I": # maybe I won't need to touch this for the next 5-10 years
        tank.rank = 1
    elif text_rank == "II":
        tank.rank = 2
    elif text_rank == "III":
        tank.rank = 3
    elif text_rank == "IV":
        tank.rank = 4
    elif text_rank == "V":
        tank.rank = 5
    elif text_rank == "VI":
        tank.rank = 6
    elif text_rank == "VII":
        tank.rank = 7
    elif text_rank == "VIII":
        tank.rank = 8
    elif text_rank == "IX":
        tank.rank = 9
    elif text_rank == "X":
        tank.rank = 10
    battle_rating  = [float(br.text.strip()) for br in soup.find(class_="general_info_br").find_all("td")[3:]]# grab all table entries, use only the last 3 as they contain the BR 
    tank.battle_rating = {"Arcade": battle_rating[0], "Realistic": battle_rating[1], "Simulator": battle_rating[2]}


def parse_vehicle_cost(tank: Tank, soup: BeautifulSoup) -> None:
    """parses the vehicles costs
    (Squadron)Research/SL/GE

    Parameters
    ----------
    tank : Tank
        the updating ground vehicle
    soup : BeautifulSoup
        data from the wiki
    """

    # Vehicle cost
    # some vehicles like pack premiums don't have both RP/SL cost, but GE Premiums have a GE cost and 
    # Squadron vehicles have both SquadronRP and SL cost
    if soup.find(class_="general_info_price_research"):
        tank.research = int(soup.find(class_="general_info_price_research").find(class_="value").text.strip().replace(" ", ""))
    if soup.find(class_="general_info_price_buy"):
        if not soup.find(class_="general_info_price_buy").find(class_="value small"): # "value small" indicates a bundle or gift premium
            tank.cost= int(soup.find(class_="general_info_price_buy").find(class_="value").text.strip().replace(" ", ""))
    if tank.is_premium and tank.research == -1: # no premium vehicle has a research kost
        tank.research = 0


def parse_vehicle_specs(tank: Tank, soup: BeautifulSoup) -> None:
    """parses the specs of an ground vehicle

    Parameters
    ----------
    tank : Tank
        the tank to be updated
    soup : BeautifulSoup
        BeautifulSoup obj containing all wiki data
    """

    # parse Armour[Hull, turret], crew, visibility
    specs = list(soup.find_all(class_="specs_info"))
    vehicle_specs = [spec for spec in specs if len(spec["class"]) == 1 ] # specs_info
    for spec in vehicle_specs:
        if spec.find(class_="name") and spec.find(class_="name").text.strip() == "Armour":
            elems = [x.text.strip() for x in spec.find_all(class_="value")]
            tank.armour_hull = dict(zip(["front", "side", "back"], [int(num) for num in elems[1].split(" / ")]))
            tank.armour_turret = dict(zip(["front", "side", "back"], [int(num) for num in elems[2].split(" / ")]))
            tank.crew = int(elems[3].split(" ")[0])
            tank.visibility = int(elems[4].replace("\xa0", " ").split(" ")[0])
        elif spec.find(class_="name") and spec.find(class_="name").text.strip() == "Repair cost":
            elems = [x.text.strip() for x in spec.find_all(class_="value")]
            if not tank.is_premium: # this is a non-premium vehicle, because you can't remove modifications from premium vehicles
                # gaijin wtf ???
                tank.repair_cost_stock = {
                    "Arcade": int(elems[1].split(" → ")[0].replace(" ", "")),
                    "Realistic": int(elems[2].split(" → ")[0].replace(" ", "")),
                    "Simulator": int(elems[3].split(" → ")[0].replace(" ", ""))
                    }
                tank.repair_cost_upgraded = {
                    "Arcade": int(elems[1].split(" → ")[1].replace(" ", "")),
                    "Realistic": int(elems[2].split(" → ")[1].replace(" ", "")),
                    "Simulator": int(elems[3].split(" → ")[1].replace(" ", ""))
                    }
                tank.total_cost_modifications_rp = int(elems[4].replace(" ", ""))
                tank.total_cost_modifications_sl = int(elems[5].replace(" ", ""))
                tank.talisman_cost = int(elems[6].replace(" ", ""))
                tank.crew_training = int(elems[7].replace(" ", ""))
                tank.rewards_sl = dict(zip(["Arcade", "Realistic", "Simulator"], [int(x) for x in elems[12].rstrip("\xa0%").split(" / ")]))
                tank.rewards_rp = dict(zip(["Arcade", "Realistic", "Simulator"], [int(x) for x in elems[13].rstrip("\xa0%").split(" / ")]))
            else:
                tank.repair_cost_stock = {"Arcade": 0, "Realistic": 0, "Simulator": 0}
                tank.repair_cost_upgraded = {
                    "Arcade": int(elems[1].replace(" ", "")),
                    "Realistic": int(elems[2].replace(" ", "")),
                    "Simulator": int(elems[3].replace(" ", ""))
                    }
                tank.crew_training = int(elems[4].replace(" ", ""))
                tank.rewards_sl = dict(zip(["Arcade", "Realistic", "Simulator"], [int(x) for x in elems[9].rstrip("\xa0%").lstrip("2 ×\xa0").split(" / ")]))
                tank.rewards_rp = dict(zip(["Arcade", "Realistic", "Simulator"], [int(x) for x in elems[10].rstrip("\xa0%").lstrip("2 ×\xa0").split(" / ")]))
        elif spec.find(class_="name") and spec.find(class_="name").text.strip() == "Speed":
            # parse weight and gears
            elems = [x.text.strip() for x in spec.find_all(class_="value")]
            tank.gears = {
                "Forward": int(elems[3].split(" ")[0]),
                "Back": int(elems[4].split(" ")[0])
                }
            tank.weight = float(elems[5].split(" ")[0])

    # parse speed, engine power, power/weight
    tables = [x for x in soup.find_all(class_="wikitable") if x.find("th")] # we only need "real" tables with [th] elems
    for specs_table in tables:
        if specs_table.find_all("th")[1].text.strip() == "Max Speed (km/h)":
            table = HTMLTableParser()
            table.feed(str(specs_table))
            specs_table = table.tables[0]
            aoa = 1 if "AoA" in specs_table[1] else 0 # AoA is Add-on Armour that can be added dynamically
            arcade = specs_table[2]
            realistic = specs_table[3][:3] + arcade[3:4+aoa] + specs_table[3][3:]
            tank.max_speed_forward = {
                "Realistic": int(realistic[1]),
                "Arcade": int(arcade[1])
                }
            tank.max_speed_reverse = {
                "Realistic": int(realistic[2]),
                "Arcade": int(arcade[2])
                }
            tank.engine_power_stock = {
                "Realistic": int(realistic[4+aoa].replace(",", "")),
                "Arcade": int(arcade[4+aoa].replace(",", ""))
                }
            tank.engine_power_upgraded = {
                "Realistic": int(realistic[5+aoa].replace(",", "")),
                "Arcade": int(arcade[5+aoa].replace(",", ""))
                }
            tank.power_to_weight_stock = {
                "Realistic": float(realistic[6+aoa]),
                "Arcade": float(arcade[6+aoa])
                }
            tank.power_to_weight_upgraded = {
                "Realistic": float(realistic[7+aoa]),
                "Arcade": float(arcade[7+aoa])
                }


def parse_vehicle_armaments(tank: Tank, soup: BeautifulSoup) -> None:
    """parses the armaments of the ground vehicle

    Parameters
    ----------
    tank : Tank
        the updated tank
    soup : BeautifulSoup
        wiki data as BS
    """
    # Armament Name Parsing
    specs = list(soup.find_all(class_="specs_info"))
    unparsed_armaments = [spec for spec in specs if len(spec["class"]) == 2] # specs_info weapons
    for armament in unparsed_armaments:
        tank.armaments.append(parse_ground_armament_name(armament))
  
    # Armament/Ammunitions Parsing
    tables = [x for x in soup.find_all(class_="wikitable") if x.find("th")] # we only need "real" tables with [th] elems
    ammunitions: List[Ammunition] = []
    for iterator in range(0, len(tables)):
        if len(tables[iterator]["class"]) == 2:
            if tables[iterator - 1].find("tr").find("th").find("a"):
                armament_name = tables[iterator - 1].find("tr").find("th").find("a").text.strip()
            #print(bytes(armament_name, encoding="utf-8"))
            if tables[iterator].find("tr").find("th").text.strip() == "Penetration statistics":
                ammunitions = parse_ground_ammunitions_pen(ammo_pen_specs=tables[iterator])
            elif tables[iterator].find("tr").find("th").text.strip() == "Shell details" and len(ammunitions):
                parse_ground_ammunitions_stats(ammo_specs=tables[iterator], ammunitions=ammunitions)
            else:
                pass
            for armament in tank.armaments:
                if armament_name in armament.name:
                    armament.ammo_types = ammunitions
        else:
            # parse the detailed armament spec
            if tables[iterator].find("th").find("a") and "mm" in tables[iterator].find("th").text: # searching for the link of an armament and "mm" in the text
                armament_name = tables[iterator].find("th").text.strip()
                for armament in tank.armaments:
                    print(f"Armament:{bytes(armament.name, encoding='utf-8')}:{bytes(armament_name, encoding='utf-8')}")
                    if armament_name in armament.name:
                        parse_ground_armament(armament, tables[iterator])


def parse_vehicles_fetures(tank: Tank, soup: BeautifulSoup) -> None:
    """parses an vehicles features

    Parameters
    ----------
    tank : Tank
        the tank to be updated
    soup : BeautifulSoup
        the data as BS
    """

    # Non-Modification Feature Parsing
    for feature in [elem.text.strip() for elem in soup.find_all(class_="feature_name")]:
        if feature == "Amphibious":
            tank.is_amphibious = True
        elif feature == "ERA":
            tank.era = True
        elif feature == "Reverse gearbox":
            tank.reverse_gearbox = True
        elif feature == "Controlled suspension":
            tank.controlled_suspension = True
        elif "stabilizer" in feature or feature == "Autoloader" : # keep this here to catch all the funky stuff
            pass
        elif feature in ["Smoke grenades", "ESS", "Laser rangefinder", "Night vision device", "Rangefinder", "Self-entrenching equipment"]: # we got those parsed already, so no need for warnings
            pass
        else:
            print(f"Feature WARN: {feature}") # add logging here

def parse_vehicle_modification_features(tank: Tank, soup: BeautifulSoup) -> None:
    """parses a tanks modification and by extend thier features

    Parameters
    ----------
    tank : Tank
        the tank to be updated
    soup : BeautifulSoup
        the wiki data as BS
    """

    # Vehicle Modification Parsing
    # ----- Get Modifications -> get specs (smokes, ess, nvd, tvd, lws, lr, rangefinder, etc...) | <div class="specs_mod">
    for mod in soup.find_all(class_="specs_mod_name"):
        if mod.text.strip() == "Smoke grenade":
            tank.smokes = True
        elif mod.text.strip() == "ESS":
            tank.ess = True
        elif mod.text.strip() == "Artillery Support":
            tank.artillery = True
        elif mod.text.strip() == "Dozer Blade":
            tank.dozer_blade = True
        elif mod.text.strip() == "Improved optics":
            tank.scouting = True
        # Visuals
        elif mod.text.strip() == "NVD":
            tank.night_vision = True
        elif mod.text.strip() == "TVD":
            tank.thermal_vision = True
        # Rangefinding
        elif mod.text.strip() == "Rangefinder":
            tank.rangefinder = True
        elif mod.text.strip() == "LR" or "Laser rangefinder":
            tank.laser_rangefinder = True
        elif mod.text.strip() == "LWS/LR":
            tank.laser_warning_rangefinder = True



def parse_ground_ammunitions_stats(ammo_specs: Tag, ammunitions: List[Ammunition]):
    """Parses Specs (Velocity, Masses, Fuse Data and Ricochet Probabilit) of Ground Vehicle Ammunition 

    Parameters
    ----------
    ammo_specs : Tag
        Ammunition Specs as BS4 Tag
    ammunitions : List[Ammunition]
        List of Ammunition Rounds
    """
    round_specs = ammo_specs.find_all("tr")[3:]
    for round in round_specs:
        for ammo in ammunitions:
            #check for ATGMs with extra range -> all other values shift by 1
            # range position: [3]
            round_data = round.find_all("td")
            if round_data[0].text.strip()!= ammo.name:
                continue
            atgm_offset = 0
            if "ATGM" in round_data[1].text.strip(): # check if the round is a ATGM missile and apply offset if needed
                atgm_offset = 1
                ammo.range = int(round_data[2].text.strip().replace(",", ""))
            ammo.velocity = int(round_data[2+atgm_offset].text.strip().replace(",", ""))
            ammo.projectile_mass = float(round_data[3+atgm_offset].text.strip().replace(",", ""))
            ammo.ricochet = dict(zip(["0%", "50%","100%"], [int(angle.text.strip().replace("°", "")) for angle in round_data[7+atgm_offset:]]))
            if not round_data[4+atgm_offset].text.strip() == "N/A":
                ammo.fuse_delay = float(round_data[4+atgm_offset].text.strip())
            if not round_data[5+atgm_offset].text.strip() == "N/A":
                ammo.fuse_sensetivity = float(round_data[5+atgm_offset].text.strip())
            if not round_data[6+atgm_offset].text.strip() == "N/A":
                ammo.explosive_mass = int(round_data[6+atgm_offset].text.strip().replace(",", "").replace(".", ""))


def parse_ground_ammunitions_pen(ammo_pen_specs: Tag) -> List[Ammunition]:
    """Parses Penetration Statistics of Ground Vehicle Ammunition

    Parameters
    ----------
    ammo_pen_specs : Tag
        Ammunition Penetration Specs as BS4 Tag

    Returns
    -------
    List[Ammunition]
        returns a Lsit of Ammunition Rounds with Penetration Statistics
    """
    ammunitions = ammo_pen_specs.find_all("tr")[3:]
    parsed_ammo: List[Ammunition] = []
    for ammo in ammunitions:
        round_name = ammo.find_all("td")[0].text.strip()
        round_type = ammo.find_all("td")[1].text.strip()
        round_pen_at_distance = dict(zip(["10", "100", "500", "1000", "1500", "2000"], [int(x.text.strip().replace(",", "")) for x in ammo.find_all("td")[2:]]))
        parsed_ammo.append(Ammunition(name=round_name, ammo_type=round_type, pen_at_distance=round_pen_at_distance))
    return parsed_ammo


def parse_ground_armament_name(armament_specs: Tag) -> Armament:
    """Parses the Armaments Name and creates a corresponding object

    Parameters
    ----------
    armament_specs : Tag
        the html containing the armaments name

    Returns
    -------
    Armament
        the armament object with it's member name parsed
    """

    armament_name = ""
    # WarThunder Wiki isn't quit sure itself if the armament name sould be placed inside an html <a> tag or not
    # but we are parsing it nonetheless
    try:
        if armament_specs.find(class_="specs_name_weapon").a:
            armament_name = armament_specs.find(class_="specs_name_weapon").a.text.strip()
        else:
            armament_name = armament_specs.find(class_="specs_name_weapon").text.strip()
    except AttributeError as excp:
        pass

    if armament_name:
        armament = Armament(name=armament_name)
        return armament
    else:
        raise AttributeError(armament_specs)


def parse_ground_armament(armament: Armament, specs_table: Tag):
    """Parses Ground Vehicle Armaments and Specs:
    Capacity
    Belt capacity
    Fire rate
    First-order Ammo Stowage
    Vertical guidance
    Horizontal Guidance
    Reload

    Parameters
    ----------
    armament : Armament
        the armament that gets it's specs updated
    specs_table : Tag
        the spces of the armament as an unparsed/unprocessed html table
    """
    table = HTMLTableParser()
    table.feed(str(specs_table))
    specs = table.tables[0]
    arcade = specs[2]
    fr_offset = 0 # there's a offset for auto-cannons as they have a fire rate
    for iterator in range(0, len(specs[1])):
        if specs[1][iterator] == "Capacity (Belt)":
            armament.capacity = int(arcade[iterator].split(" ")[0].replace(",", ""))
            armament.belt_capacity = int(arcade[iterator].split("(")[1].rstrip(")").replace(",", ""))
        elif specs[1][iterator] == "Fire rate":
            armament.fire_rate = int(arcade[iterator].replace(",", ""))
            fr_offset = fr_offset + 1
        elif specs[1][iterator] == "Capacity":
            armament.capacity = int(arcade[iterator].split(" ")[0].replace(",", ""))
        elif specs[1][iterator] == "Vertical":
            armament.vertical_guidance = parse_vertical_guidance(guidance_value=arcade[iterator])
        elif specs[1][iterator] == "Stabilizer":
            armament.stabilizer = get_stabilizer_type(arcade[iterator])
    if len(specs[1]) > 10: # expect that this is now a larger caliber "main armament"
        # "equalize" both arcade and realistic tables
        realistic = ["Realistic"] + arcade[1:5] + specs[3][1:] + arcade[10:]
        armament.reload_time = {
            "stock":float(arcade[10+fr_offset]),
            "full": float(arcade[11+fr_offset]),
            "expert": float(arcade[11+fr_offset]),
            "aces": float(arcade[13+fr_offset])
            }
        armament.rotation_speed_arcade = {
            "stock": float(arcade[5+fr_offset]),
            "upgraded": float(arcade[6+fr_offset]),
            "full": float(arcade[7+fr_offset]),
            "expert": float(arcade[8+fr_offset]),
            "aces": float(arcade[9+fr_offset])
            }
        armament.rotation_speed_realistic = {
            "stock": float(realistic[5+fr_offset]),
            "upgraded": float(realistic[6+fr_offset]),
            "full": float(realistic[7+fr_offset]),
            "expert": float(realistic[8+fr_offset]),
            "aces": float(realistic[9+fr_offset])
            }
    elif len(specs[1]) > 5 and len(specs[1]) < 10: # sumsum little special for secondary non-rotatable armaments
        if specs[1][1] == "Mode" or specs[1][1] == "Mount":
            fr_offset = fr_offset + 1
        armament.reload_time = {
            "stock":float(arcade[4+fr_offset]),
            "full": float(arcade[5+fr_offset]),
            "expert": float(arcade[6+fr_offset]),
            "aces": float(arcade[7+fr_offset])
            }

    print(armament.__dict__)

def get_stabilizer_type(stablizer_string: str) -> Stabilizer:
    """parses the stabilizer type for an armament

    Parameters
    ----------
    stablizer_string : str
        string containing the stabilizer type

    Returns
    -------
    Stabilizer
        returns the stabilizer type as enum
    """
    if stablizer_string == "Two-plane":
        return Stabilizer.TWOPLANE
    elif stablizer_string == "Vertical":
        return Stabilizer.VERTICAL
    elif stablizer_string == "Shoulder":
        return Stabilizer.SHOULDER
    elif stablizer_string == "N/A":
        return Stabilizer.NONE
    else:
        print(f"Armament Feature WARN: {stablizer_string}") # add logging here
        return Stabilizer.NONE

        
def parse_vertical_guidance(guidance_value: str) -> Dict[str, int]:
    """Parses the Vertical Guidance of an armament

    Parameters
    ----------
    guidance_value : str
        string containing the vertical guidance -X/X°

    Returns
    -------
    Dict[str, int]
        returns a sorted dict containing the minimum/maximum guidance
    """
    if guidance_value == "N/A":
        return {"positive": 0, "negative": 0}
    guidances = [int(x) for x in guidance_value.replace("°", "").split("/")]
    if guidances[0] > guidances[1]:
        return {"positive": guidances[0], "negative": guidances[1]}
    else:
        return {"positive": guidances[1], "negative": guidances[0]}

    
def __main__():
    """Main-ly used for standalone testing during developemnt
    """
    content: str
    test_vehicles = [
        "AML-90_(Israel)", # Name parsing Israeal
        "Magach_3_(USA)", # Name Parsing USA, Pack Premium
        "Maus", # Multi Cannon
        "M24_(Italy)", # Vertical Stabilizer, Name Parsing Italy
        "Pz.Kpfw._Churchill_(Germany)", # "Shoulder Stabilizer", German Name Parsing
        "Type_62_(USSR)", # NAme Parsing USSR
        "Sho't_Kal_Dalet_(Great_Britain)", # Name Parsing GB
        "M47_(Japan)", # Name Parsing JP, Rangefinder
        "PT-76_(China)", # Name Parsing Taiwan
        "ItO_90M_(France)", # Name Parsing France
        "Bkan_1C", # Reverse Gearbox
        "AMX-10RC", # Suspension
        "Object_685", # Amphibious, Autoloader
        "T-72AV_(TURMS-T)", # ERA, ESS, Dozer Blades
        "Centauro_I_105", # LWS, Thermals
        "ADATS_(M113)", # ATGM
        "BMP-2M", # Squadron
        "ZSU-23-4", # Radar in Wiki
        "SIDAM_25", # Optotronics
        "VEAK_40", # Radar not in Wiki
        "AMX-30B2_BRENUS", # passive APS
        "Black_Night", # Active APS
        "M113A1_(TOW)", # fire on the move 5km/h
        "Strv_81_(RB_52)", # tank with missel launcher
        "M901", # lowes fire while moving speed found (1km/h)
        # "M60A1_\"D.C.Ariete\"", # GE Premium
        # "AUBL/74_HVG" # Marketplace Vehicle
    ]
    for vehicle in test_vehicles:
        test_tank_file_name = f"Test_Vehicles\\{vehicle}.html"
        with open(test_tank_file_name, "r", encoding="utf-8") as data:
            content = data.read()
        parse_ground_vehicle(response_content=content)

if __name__ == "__main__":
    __main__()