"""Parsing of Ground Vehicles using data provided by the WarThunder Wiki
"""

from bs4 import BeautifulSoup, SoupStrainer, Tag
from ammunition import Ammunition
from armament import Armament
from tanks import Tank
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
    # ATGMS !?
    # Horizontal Guidance
    # Rank
    # BR
    # Radar
    # Scout
    # ERA
    # Variable Suspension ? (hydropneumatic suspension)

    soup = BeautifulSoup(response_content, "html.parser", parse_only=SoupStrainer(class_="mw-parser-output"))
    specs = list(soup.find_all(class_="specs_info"))
    unparsed_armaments: List[Armament] = []

    # Armament Parsing
    unparsed_armaments = [spec for spec in specs if len(spec["class"]) == 2]
    specs = [spec for spec in specs if len(spec["class"]) == 1 ]
    parsed_tank = Tank("Tank1")
    for armament in unparsed_armaments:
        parsed_tank.armaments.append(parse_ground_armaments(armament))
  
    # Ammunitions Parsing
    tables = soup.find_all(class_="wikitable")
    ammunitions: List[Ammunition] = []
    for iterator in range(0, len(tables)):
        if len(tables[iterator]["class"]) == 2:
            armament_name = tables[iterator - 1].find("tr").find("th").text.strip("n").strip()
            if tables[iterator].find("tr").find("th").text == "Penetration statistics":
                ammunitions = parse_ground_ammunitions_pen(ammo_pen_specs=tables[iterator])
            elif tables[iterator].find("tr").find("th").text == "Shell details" and len(ammunitions):
                parse_ground_ammunitions_stats(ammo_specs=tables[iterator], ammunitions=ammunitions)
            else:
                pass
            for armament in parsed_tank.armaments:
                if armament_name in armament.name:
                    armament.ammo_types = ammunitions

    for armament in parsed_tank.armaments:
        print(armament.__str__())

    # Vehicle Spec Parsing
    for spec in specs:
        pass

    # class_="feature_name"

    # Vehicle Modification Parsing
    # ----- Get Modifications -> get specs (smokes, ess, nvd, tvd, lws, lr, rangefinder, etc...) | <div class="specs_mod">
    mods = soup.find_all(class_="specs_mod_name")
    for mod in mods:
        if mod.text == "Smoke grenade":
            parsed_tank.smokes = True
        elif mod.text == "ESS":
            parsed_tank.ess = True
        elif mod.text == "Artillery Support":
            parsed_tank.artillery = True
        elif mod.text == "Dozer Blade":
            parsed_tank.dozer_blade = True
        elif mod.text == "NVD":
            parsed_tank.night_vision = True
        elif mod.text == "TVD":
            parsed_tank.thermal_vision = True
        elif mod.text == "Rangefinder":
            parsed_tank.rangefinder = True
        elif mod.text == "LR":
            parsed_tank.laser_rangefinder = True
        elif mod.text == "LWS/LR":
            parsed_tank.laser_warning_rangefinder = True



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
            round_data = round.find_all("td")
            if round_data[0].text != ammo.name:
                continue
            ammo.velocity = int(round_data[2].text.replace(",", ""))
            ammo.projectile_mass = float(round_data[3].text.replace(",", ""))
            ammo.ricochet = dict(zip(["0%", "50%","100%"], [int(angle.text.replace("°", "")) for angle in round_data[7:]]))
            if not round_data[4].text == "N/A":
                ammo.fuse_delay = float(round_data[4].text)
            if not round_data[5].text == "N/A":
                ammo.fuse_sensetivity = float(round_data[5].text)
            if not round_data[6].text == "N/A":
                ammo.explosive_mass = float(round_data[6].text.replace(",", ""))



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
        round_name = ammo.find_all("td")[0].text
        round_type = ammo.find_all("td")[1].text
        round_pen_at_distance = dict(zip(["10", "100", "500", "1000", "1500", "2000"], [int(x.text) for x in ammo.find_all("td")[2:]]))
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
    armament = Armament(armament_specs.find(class_="specs_name_weapon").a.text)
    for stat in armament_specs.find_all(class_="specs_char_block"):
        if stat.find(class_="name").text == "Belt capacity":
            print("BCap")
            armament.belt_capacity = int(stat.find(class_="value").text.split(" rounds")[0].replace(" ", ""))
        elif stat.find(class_="name").text == "Ammunition":
            print("Cap")
            armament.capacity = int(stat.find(class_="value").text.split(" rounds")[0].replace(" ", ""))
        elif stat.find(class_="name").text == "Fire rate":
            print("Rate")
            armament.fire_rate = int(stat.find(class_="value").text.split(" shots")[0].replace(" ", ""))
        elif stat.find(class_="name").text == "First-order":
            print("Stowage")
            armament.first_stowage = int(stat.find(class_="value").text.split(" rounds")[0].replace(" ", ""))
        elif stat.find(class_="name").text == "Vertical guidance":
            print("guidance")
            guidances = [int(x) for x in stat.find(class_="value").text.replace("°", "").split(" / ")]
            if guidances[0] > guidances[1]:
                armament.vertical_guidance = {"positive": guidances[0], "negative": guidances[1]}
            else:
                armament.vertical_guidance = {"positive": guidances[1], "negative": guidances[0]}
        elif stat.find(class_="name").text == "Reload":
            print("reloads")
            reloads = [float(x) for x in stat.find(class_="specs_char_line indent").find(class_="value").text.rstrip(" s").split(" → ")]
            if reloads[0] > reloads[1]:
                armament.reload_time = {"basic": reloads[0], "aces": reloads[1]}
            else:
                armament.reload_time = {"basic": reloads[1], "aces": reloads[0]}

    print(armament.__dict__)
    return armament



def __main__():
    """Main-ly used for standalone testing during developemnt
    """
    content: str
    #test_tank_file_name = "Maus.html"
    test_tank_file_name = "Magach_3_(USA).html"
    with open(test_tank_file_name, "r", encoding="utf-8") as data:
        content = data.read()
    #print(content)
    parse_ground_vehicle(response_content=content, html_tag="")

if __name__ == "__main__":
    __main__()