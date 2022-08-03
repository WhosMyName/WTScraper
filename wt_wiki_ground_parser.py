"""Parsing of Ground Vehicles using data provided by the WarThunder Wiki
"""

from bs4 import BeautifulSoup, SoupStrainer, Tag
from ammunition import Ammunition
from armament import Armament, Stabilizer
from tanks import Tank, VehicleClass
from typing import List


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
    # Horizontal Guidance
    # Radar
    # APS ?
    # Composite armour

    soup = BeautifulSoup(response_content, "html.parser", parse_only=SoupStrainer(class_="mw-parser-output"))
    specs = list(soup.find_all(class_="specs_info"))
    unparsed_armaments: List[Armament] = []

    # General Tank Parsing (Name, VehicleClass, Premium, Squadron)
    parsed_tank = Tank(name=soup.find(class_="general_info_name").text)
    parsed_tank.is_squadron = True if soup.find(class_="squadron") else False
    parsed_tank.is_premium = True if soup.find(class_="premium") else False
    if parsed_tank.is_squadron:
        soup.find(class_="squadron").extract()
    if parsed_tank.is_premium:
        soup.find(class_="premium").extract()
    vehicle_class = soup.find(class_="general_info_class").find("a").text.strip() # checking if the vehicle is of a certiain class and/or premium/squadron
    if vehicle_class == "Light tank":
        parsed_tank.vehicle_class = VehicleClass.LIGHT
    elif vehicle_class == "Medium tank":
        parsed_tank.vehicle_class = VehicleClass.MEDIUM
    elif vehicle_class == "Heavy tank":
        parsed_tank.vehicle_class = VehicleClass.HEAVY
    elif vehicle_class == "SPAA":
        parsed_tank.vehicle_class = VehicleClass.SPAA
    elif vehicle_class == "Tank destroyer":
        parsed_tank.vehicle_class = VehicleClass.TANK_DESTROYER
    else:
        print(f"{parsed_tank.name}: {vehicle_class}")

    # Battle Rating, Rank, Nation
    parsed_tank.nation = soup.find(class_="general_info_nation").find_all("a")[-1].text.strip()
    text_rank = soup.find(class_="general_info_rank").a.text.strip().split(" ")[0] # "V Rank"
    if text_rank == "I": # maybe I won't need to touch this for the next 5-10 years
        parsed_tank.rank = 1
    elif text_rank == "II":
        parsed_tank.rank = 2
    elif text_rank == "III":
        parsed_tank.rank = 3
    elif text_rank == "IV":
        parsed_tank.rank = 4
    elif text_rank == "V":
        parsed_tank.rank = 5
    elif text_rank == "VI":
        parsed_tank.rank = 6
    elif text_rank == "VII":
        parsed_tank.rank = 7
    elif text_rank == "VIII":
        parsed_tank.rank = 8
    elif text_rank == "IX":
        parsed_tank.rank = 9
    elif text_rank == "X":
        parsed_tank.rank = 10
    battle_rating  = [float(br.text.strip()) for br in soup.find(class_="general_info_br").find_all("td")[3:]]# grab all table entries, use only the last 3 as they contain the BR 
    parsed_tank.battle_rating = {"AB": battle_rating[0], "RB": battle_rating[1], "SB": battle_rating[2]}

    # Armament Parsing
    unparsed_armaments = [spec for spec in specs if len(spec["class"]) == 2] # specs_info weapons
    for armament in unparsed_armaments:
        parsed_tank.armaments.append(parse_ground_armaments(armament))
  
    # Ammunitions Parsing
    
    #statistics = [elem for elem in soup.find_all(class_="wikitable") if len(elem["class"]) == 1]
    #tables = [elem for elem in soup.find_all(class_="wikitable") if len(elem["class"]) == 2]
    tables = soup.find_all(class_="wikitable")
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
            for armament in parsed_tank.armaments:
                #print(f"Armament:{bytes(armament.name, encoding='utf-8')}:{bytes(armament_name, encoding='utf-8')}")
                if armament_name in armament.name:
                    armament.ammo_types = ammunitions
        else:
            # parse the turret rotation speed if any
            for elem in tables[iterator].find_all("th"):
                if "Turret rotation speed" in elem.text.strip():
                    pass
                    # 4-8

    # Vehicle Spec Parsing
    specs = [spec for spec in specs if len(spec["class"]) == 1 ] # specs_info
    for spec in specs:
        #print(f"{spec}\n\n")
        pass
        # parse Armour, Hull, turret, crew, visibility
        # parse speed, gears, weight, engine power, power/weight
        # parse repair cost, crew training, battle reward, 



    for feature in soup.find_all(class_="feature_name"):
        if feature.text.strip() == "Amphibious":
            parsed_tank.is_amphibious = True
        elif feature.text.strip() == "ERA":
            parsed_tank.era = True
        elif feature.text.strip() == "Reverse gearbox":
            parsed_tank.reverse_gearbox = True
        elif feature.text.strip() == "Controlled suspension":
            parsed_tank.controlled_suspension = True
        elif "stabilizer" in feature.text.strip() or feature.text.strip() == "Autoloader" : # keep this here to catch all the funky stuff
            pass
        elif feature.text.strip() in ["Smoke grenades", "ESS", "Laser rangefinder", "Night vision device", "Rangefinder", "Self-entrenching equipment"]: # we got those parsed already, so no need for warnings
            pass
        else:
            print(f"Feature WARN: {feature.text.strip()}") # add logging here


    # Vehicle Modification Parsing
    # ----- Get Modifications -> get specs (smokes, ess, nvd, tvd, lws, lr, rangefinder, etc...) | <div class="specs_mod">
    # in extra funktion auslagern # def parse_ground_vehicle_modifications(Tank, )
    for mod in soup.find_all(class_="specs_mod_name"):
        if mod.text.strip() == "Smoke grenade":
            parsed_tank.smokes = True
        elif mod.text.strip() == "ESS":
            parsed_tank.ess = True
        elif mod.text.strip() == "Artillery Support":
            parsed_tank.artillery = True
        elif mod.text.strip() == "Dozer Blade":
            parsed_tank.dozer_blade = True
        elif mod.text.strip() == "Improved optics":
            parsed_tank.scouting = True
        # Visuals
        elif mod.text.strip() == "NVD":
            parsed_tank.night_vision = True
        elif mod.text.strip() == "TVD":
            parsed_tank.thermal_vision = True
        # Rangefinding
        elif mod.text.strip() == "Rangefinder":
            parsed_tank.rangefinder = True
        elif mod.text.strip() == "LR":
            parsed_tank.laser_rangefinder = True
        elif mod.text.strip() == "LWS/LR":
            parsed_tank.laser_warning_rangefinder = True

    print(parsed_tank.__str__())



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
            ammo.velocity = int(round_data[2+atgm_offset].text.replace(",", ""))
            ammo.projectile_mass = float(round_data[3+atgm_offset].text.replace(",", ""))
            ammo.ricochet = dict(zip(["0%", "50%","100%"], [int(angle.text.replace("°", "")) for angle in round_data[7+atgm_offset:]]))
            if not round_data[4+atgm_offset].text.strip() == "N/A":
                ammo.fuse_delay = float(round_data[4+atgm_offset].text)
            if not round_data[5+atgm_offset].text.strip() == "N/A":
                ammo.fuse_sensetivity = float(round_data[5+atgm_offset].text)
            if not round_data[6+atgm_offset].text.strip() == "N/A":
                ammo.explosive_mass = int(round_data[6+atgm_offset].text.replace(",", ""))



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


def parse_ground_armaments(armament_specs: Tag) -> Armament:
    """Parses Ground Vehicle Armaments and Specs:
    Capacity
    Belt capacity
    Fire rate
    First-order Ammo Stowage
    Vertical guidance
    Reload

    Parameters
    ----------
    armament_specs : Tag
        _description_

    Returns
    -------
    Armament
        _description_
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

    armament = Armament(name=armament_name)
    for stat in armament_specs.find_all(class_="specs_char_block"):
        if stat.find(class_="name").text.strip() == "Belt capacity":
            armament.belt_capacity = int(stat.find(class_="value").text.split(" rounds")[0].replace(" ", ""))
        elif stat.find(class_="name").text.strip() == "Ammunition":
            armament.capacity = int(stat.find(class_="value").text.split(" rounds")[0].replace(" ", ""))
        elif stat.find(class_="name").text.strip() == "Fire rate":
            armament.fire_rate = int(stat.find(class_="value").text.split(" shots")[0].replace(" ", ""))
        elif stat.find(class_="name").text.strip() == "First-order":
            armament.first_stowage = int(stat.find(class_="value").text.split(" rounds")[0].replace(" ", ""))
        elif stat.find(class_="name").text.strip() == "Vertical guidance":
            guidances = [int(x) for x in stat.find(class_="value").text.replace("°", "").split(" / ")]
            if guidances[0] > guidances[1]:
                armament.vertical_guidance = {"positive": guidances[0], "negative": guidances[1]}
            else:
                armament.vertical_guidance = {"positive": guidances[1], "negative": guidances[0]}
        elif stat.find(class_="name").text.strip() == "Reload":
            try:
                if stat.find(class_="specs_char_line indent"): # i'd guess this case is used if there's no autoloader
                    reloads = [float(x) for x in stat.find(class_="specs_char_line indent").find(class_="value").text.rstrip(" s").split(" → ")]
                else:
                    reloads = [float(x) for x in stat.find(class_="value").text.rstrip(" s").split(" → ")]
            except AttributeError as excp:
                pass

            if len(reloads) > 1: # reloads improve with crew skill
                if reloads[0] > reloads[1]:
                    armament.reload_time = {"basic": reloads[0], "aces": reloads[1]}
                else:
                    armament.reload_time = {"basic": reloads[1], "aces": reloads[0]}
            else: # except when using autoloaders
                armament.autoloader = True
                armament.reload_time = {"basic": reloads[0], "aces": reloads[0]}

    # parse all the stabilizers, as they are "features" of the armament
    for feature in armament_specs.find_all(class_="feature_name"):
        if feature.text.strip() == "Autoloader": # keep this here so we can catch some fancy stuff in the auto-m8'd phase
            pass
        elif feature.text.strip() == "Two-plane stabilizer":
            armament.stabilizer = Stabilizer.TWOPLANE
        elif feature.text.strip() == "Vertical stabilizer":
            armament.stabilizer = Stabilizer.VERTICAL
        elif feature.text.strip() == "Shoulder stabilizer":
            armament.stabilizer = Stabilizer.SHOULDER
        else:
            print(f"Armament Feature WARN: {feature.text.strip()}") # add logging here

    return armament



def __main__():
    """Main-ly used for standalone testing during developemnt
    """
    content: str
    test_vehicles = [
        # "M24_(Italy)", # Vertical Stabilizer, Name Parsing Italy
        # "AML-90_(Israel)", # Name parsing Israeal
        # "Magach_3_(USA)", # Name Parsing USA
        # "Maus", # Multi Cannon
        # "Pz.Kpfw._Churchill_(Germany)", # "Shoulder Stabilizer", German Name Parsing
        # "Type_62_(USSR)", # Name Parsing USSR
        # "Sho't_Kal_Dalet_(Great_Britain)", # Name Parsing GB
        # "M47_(Japan)", # Name Parsing JP, Rangefinder
        # "PT-76_(China)", # Name Parsing Taiwan
        # "ItO_90M_(France)", # Name Parsing France
        # "Bkan_1C", # Reverse Gearbox
        "AMX-10RC", # Suspension
        # "Object_685", # Amphibious, Autoloader
        # "T-72AV_(TURMS-T)", # ERA, ESS, Dozer Blades
        # "Centauro_I_105", # LWS, Thermals
        # "ADATS_(M113)", # ATGM
        # "BMP-2M", # Squadron
        # "ZSU-23-4", # Radar in Wiki
        # "SIDAM_25", # Optotronics
        # "VEAK_40", # Radar not in Wiki
    ]
    for vehicle in test_vehicles:
        test_tank_file_name = f"Test_Vehicles\\{vehicle}.html"
        with open(test_tank_file_name, "r", encoding="utf-8") as data:
            content = data.read()
        parse_ground_vehicle(response_content=content)

if __name__ == "__main__":
    __main__()