from bs4 import BeautifulSoup, SoupStrainer, Tag


def parser_XYZ_vehicle(response_content: str, html_tag: str):
    pass


def parser_ground_vehicle(response_content: str, html_tag: str):
    soup = BeautifulSoup(response_content, "html.parser", parse_only=SoupStrainer(class_="mw-normal-catlinks"))
    



def parse_ground_specs(response_content: str) -> str:



def __main__():
    content: str
    with open("Magach_3_(USA).html", "r", encoding="utf-8") as data:
        content = data.read()
    print(content)

if __name__ == "__main__":
    __main__()