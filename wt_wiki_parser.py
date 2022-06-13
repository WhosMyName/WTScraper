from bs4 import BeautifulSoup, SoupStrainer, Tag
from ammunition import Ammunition
from armament import Armament
from tanks import Tank
from typing import List


def parser_XYZ_vehicle(response_content: str, html_tag: str):
    pass


def parser_ground_vehicle(response_content: str, html_tag: str) -> Tank:
    soup = BeautifulSoup(response_content, "html.parser", parse_only=SoupStrainer(class_="mw-parser-output"))
    specs = list(soup.find_all(class_="specs_info"))
    armaments = []
    for spec in specs: # increase efficiency by list comprehensions thing
        print(spec["class"])
        if len(spec["class"]) == 2 and spec["class"][1] == "weapon": # if spec["class"][0] == "specs_info weapon":
            armaments.append(spec)
    specs = [spec for spec in specs if len(spec["class"]) == 1 ]
    parsed_tank = Tank("Tank1")
    #for armament in armaments:
    #    parsed_tank.armaments.append(parse_ground_armaments(armament))

    tables = soup.find_all(class_="wikitable sortable")
    ammunitions: List[Ammunition]
    for table in tables:
        if table.find("tr").find("th").text == "Penetration statistics":
            ammunitions = parse_ground_ammunitions_pen(table)
        elif table.find("tr").find("th").text == "Shell details" and len(ammunitions):
            parse_ground_ammunitions_stats(ammo_specs=table, ammunitions=ammunitions)
        else:
            pass


def parse_ground_ammunitions_stats(ammo_specs: Tag, ammunitions: List[Ammunition]):
    pass


def parse_ground_ammunitions_pen(ammo_pen_specs: Tag) -> List[Ammunition]:
    ammunitions = ammo_pen_specs.find_all("tr")[3:]
    parsed_ammo: List[Ammunition] = []
    for ammo in ammunitions:
        round_name = ammo.find_all("td")[0].text
        round_type = ammo.find_all("td")[1].text
        round_pen_at_distance = dict(zip(["10", "100", "500", "1000", "1500", "2000"], [int(x.text) for x in ammo.find_all("td")[2:]]))
        parsed_ammo.append(Ammunition(name=round_name, ammo_type=round_type, pen_at_distance=round_pen_at_distance))
    return parsed_ammo


def parse_ground_armaments(armament_specs: Tag) -> Armament:
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



def parse_ground_specs(response_content: str) -> str:
    pass



def __main__():
    content: str
    with open("Magach_3_(USA).html", "r", encoding="utf-8") as data:
        content = data.read()
    #print(content)
    parser_ground_vehicle(response_content=content, html_tag="")

if __name__ == "__main__":
    __main__()