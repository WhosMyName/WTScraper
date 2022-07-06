"""Scrapes the WarThunder Wiki for all availible Vehicles for all Nations for all Environments (Earth, Wind and Not Fire!)
Dumps all parsed vehiles in a file (database)

Returns
-------
_type_
    Happiness
"""

# import DB
from typing import Dict
import requests
from bs4 import BeautifulSoup, SoupStrainer, Tag

BASE_URL = f"https://wiki.warthunder.com"

def get_aviation_nations() -> Dict[str, str]:
    """Requests aviation data for further parsing

    Returns
    -------
    Dict[str, str]
        Dict with nation's name as key and their aviation tech tree URL as value
    """
    aviation_url = f"{BASE_URL}/Aviation"
    content = requests.get(aviation_url).text
    return get_nation(content=content)


def get_ground_nations() -> Dict[str, str]:
    """Requests ground data for further parsing

    Returns
    -------
    Dict[str, str]
        Dict with nation's name as key and their ground tech tree URL as value
    """
    ground_url = f"{BASE_URL}/Ground_vehicles"
    content = requests.get(ground_url).text
    return get_nation(content=content)


def get_fleet_nations() -> Dict[str, str]:
    """Requests fleet data for further parsing

    Returns
    -------
    Dict[str, str]
        Dict with nation's name as key and their fleet tech tree URL as value
    """
    fleet_url = f"{BASE_URL}/Fleet"
    content = requests.get(fleet_url).text
    return get_nation(content=content)


def get_nation(content: str) -> Dict[str, str]:
    """Parses all availible Nations for an given Environment

    Parameters
    ----------
    content : str
        Environment-based URL for all nations

    Returns
    -------
    Dict[str, str]
        Dict with nation's name as key and their tech tree URL as value
    """
    soup = BeautifulSoup(content, "html.parser", parse_only=SoupStrainer(class_="wt-class-table"))
    nations_divs = soup.find_all("tr")[0].find_all("a")[1::2]
    url_list = {}
    for div in nations_divs:
        url_list[div.string] = f"{BASE_URL}{div['href']}"
    return url_list


def get_vehicles_by_nation(nation_url: str) -> Dict[str, str]:
    """Parses a nations vehicles

    Parameters
    ----------
    nation_url : str
        the URL of a nation for any given environment type (air, ground, water)

    Returns
    -------
    Dict[str, str]
        Dict containing a vehicles name as key and the corresponding URL as value
    """
    content = requests.get(nation_url).text
    soup = BeautifulSoup(content, "html.parser", parse_only=SoupStrainer(class_="mw-category"))
    vehicle_list = {}
    for group in soup.find_all(class_="mw-category-group"):
        for list_entry in group.ul:
            if type(list_entry) == Tag:
                vehicle_list[list_entry.a.string] = f"{BASE_URL}{list_entry.a['href']}"
    return vehicle_list

def get_vehicle_specs(vehicle_url: str): # WIP
    """Grabs specific vehicles from the wiki, passes them to the parser and (pushes them to the DB)

    Currently just saves the data to a html file for offline prosessing during developemnt.

    Parameters
    ----------
    vehicle_url : str
        URL of a specific vehicle

    Returns
    -------
    _type_ [Vehicle]
        Model of the specified Vehicle
    """
    content = requests.get(vehicle_url).text
    soup = BeautifulSoup(content, "html.parser", parse_only=SoupStrainer(class_="mw-normal-catlinks"))
    with open(f"{vehicle_url.split('/')[len(vehicle_url.split('/')) - 1]}.html", "w", encoding="utf-8") as vec:
        vec.write(content)
    if "ground" in soup.ul.li.string.lower():
        print("Earth")
    elif "aviation" in soup.ul.li.string.lower():
        print("Wind")
    elif "fleet" in soup.ul.li.string.lower():
        print("Not Fire!")
    else:
        return None


def __main__():
    """Main
    """
    #get_vehicles_by_nation(get_aviation_nations().pop("USA"))
    #get_vehicles_by_nation(get_fleet_nations().pop("USA"))
    #get_vehicles_by_nation(get_ground_nations().pop("USA"))
    test_vehicles = [
        "AML-90_(Israel)", # Name parsing Israeal
        "Magach_3_(USA)", # Name Parsing USA
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
        "ZSU-23-4", # Radar in Wiki
        "SIDAM_25", # Optotronics
        "VEAK_40", # Radar not in Wiki
        "AMX-30B2_BRENUS", # passive APS
        "Black_Night", # Active APS
        "M113A1_(TOW)", # fire on the move 5km/h
        "Strv_81_(RB_52)", # tank with missel launcher
        "M901" # lowes fire while moving speed found (1km/h)
    ]
    for vehicle in test_vehicles:
        get_vehicle_specs(f"https://wiki.warthunder.com/{vehicle}")

if __name__ == "__main__":
    __main__()