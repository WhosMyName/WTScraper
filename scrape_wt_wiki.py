# scrape_wt_wiki

# import DB
from tabnanny import verbose
from typing import Dict, List
import requests
from bs4 import BeautifulSoup, SoupStrainer, Tag

BASE_URL = f"https://wiki.warthunder.com"

def get_aviation_nations() -> Dict[str, str]:
    aviation_url = f"{BASE_URL}/Aviation"
    content = requests.get(aviation_url).text
    return get_nation(content=content)


def get_ground_nations() -> Dict[str, str]:
    ground_url = f"{BASE_URL}/Ground_vehicles"
    content = requests.get(ground_url).text
    return get_nation(content=content)


def get_fleet_nations() -> Dict[str, str]:
    fleet_url = f"{BASE_URL}/Fleet"
    content = requests.get(fleet_url).text
    return get_nation(content=content)


def get_nation(content: str) -> Dict[str, str]:
    soup = BeautifulSoup(content, "html.parser", parse_only=SoupStrainer(class_="wt-class-table"))
    nations_divs = soup.find_all("tr")[0].find_all("a")[1::2]
    url_list = {}
    for div in nations_divs:
        url_list[div.string] = fleet_url = f"{BASE_URL}{div['href']}"
    return url_list


def get_vehicles_by_nation(nation_url: str) -> Dict[str, str]:
    content = requests.get(nation_url).text
    soup = BeautifulSoup(content, "html.parser", parse_only=SoupStrainer(class_="mw-category"))
    vehicle_list = {}
    for group in soup.find_all(class_="mw-category-group"):
        for list_entry in group.ul:
            if type(list_entry) == Tag:
                vehicle_list[list_entry.a.string] = f"{BASE_URL}{list_entry.a['href']}"
    return vehicle_list

def get_vehicle_specs(vehicle_url: str):
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
    #get_vehicles_by_nation(get_aviation_nations().pop("USA"))
    #get_vehicles_by_nation(get_fleet_nations().pop("USA"))
    #get_vehicles_by_nation(get_ground_nations().pop("USA"))
    get_vehicle_specs("https://wiki.warthunder.com/Maus")
    #get_vehicle_specs("https://wiki.warthunder.com/F-84B-26")
    #get_vehicle_specs("https://wiki.warthunder.com/Kim_Qui")

if __name__ == "__main__":
    __main__()