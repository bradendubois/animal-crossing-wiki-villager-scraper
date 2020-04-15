from requests import get
from bs4 import BeautifulSoup

import urllib.request



villager_list = ["/wiki/Zucker"] # get_villager_list()


wiki_url = "https://animalcrossing.fandom.com"

total_villager_data = {}

for villager in villager_list:

    village_local_name = villager.replace("/wiki/",  "")

    # Get the page and parse it with BeautifulSoup
    response = get(wiki_url + villager)
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
    villager_data["name_en"] = names[0].getText()
    villager_data["name_jp"] = names[1].getText()

    # Clean and store the figure data
    high_res_image_url = figure.find_all("a")[0].get("href")
    caption = figure.find_all("figcaption")[0].getText()
    urllib.request.urlretrieve(high_res_image_url, village_local_name + ".jpg")
    villager_data["caption"] = caption

    # Clean and store the attribute data
    for attribute in attributes:

        key = attribute.find_all("h3")[0].getText()
        value = attribute.find_all("div")[0]

        if key == "Birthday":
            elements = value.find_all("a")

            birthday = elements[0].getText()
            star_sign = elements[1].getText()

            values = [birthday, star_sign]
        elif key == "Initial phrase":
            values = value.find(text=True, recursive=False).strip()
        elif key == "Initial clothes":
            values = []
            for v in value.find_all("sup", recursive=False):
                values.append(v.previous_sibling + " " + v.getText())
        else:
            values = [v.strip() for v in value.getText().split(",")]

        villager_data[key.lower()] = values

    print(villager_data)
