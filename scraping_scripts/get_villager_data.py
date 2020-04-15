import urllib

from requests import get
from bs4 import BeautifulSoup
from urllib import request

wiki_url = "https://animalcrossing.fandom.com/wiki/"


def get_villager_data(villager_name: str):
    """
    Scrape all the data for a given villager from the Animal Crossing Fandom wiki.
    Also saves the image associated with a given villager in a folder
    :param villager_name: the name of the villager, i.e. "Zucker"
    :return: A dictionary of all the data scraped for the respective villager
    """

    # Get the page and parse it with BeautifulSoup
    response = get(wiki_url + villager_name)
    soup_response = BeautifulSoup(response.text, 'html.parser')

    # Will store the data as a dictionary and write it as JSON later
    villager_data = {}

    # The "aside" is an HTML element containing all the important villager information
    aside = soup_response.findAll("aside")[0]

    # Get all the data for this villager
    names = aside.find_all("h2", {"class": "pi-item pi-item-spacing pi-title"})
    figure = aside.find_all("figure", {"class": "pi-item pi-image"})[0]
    attributes = aside.find_all("div", {"class": "pi-item pi-data pi-item-spacing pi-border-color"})

    # Clean and store names
    cleaned_names = [name.getText() for name in names]

    villager_data["name_en"] = cleaned_names[0]
    if len(cleaned_names) > 1:
        villager_data["name_jp"] = cleaned_names[1]

    # Clean and store the figure data
    high_res_image_url = figure.find_all("a")[0].get("href")
    caption = figure.find_all("figcaption")
    urllib.request.urlretrieve(high_res_image_url, "villager-data/images/" + villager_name + ".jpg")
    if len(caption) > 0:
        villager_data["caption"] = caption[0].getText()

    # Clean and store the attribute data
    for attribute in attributes:

        key = attribute.find_all("h3")[0].getText()
        value = attribute.find_all("div")[0]

        if key == "Birthday":
            values = [v.getText() for v in value.find_all("a", recursive=False)]
        elif key == "Initial phrase":
            values = value.find(text=True, recursive=False).strip()
        elif key == "Initial clothes":
            values = [element.strip() for element in value.getText().split(")")]
            for index in range(len(values)):
                if "(" in values[index]:
                    values[index] = values[index] + ")"
            values = [element for element in values if element]
        else:
            values = value.getText()
            if "," in values:
                values = [v.strip() for v in values.split(",")]

        villager_data[key.lower()] = values

    return villager_data
