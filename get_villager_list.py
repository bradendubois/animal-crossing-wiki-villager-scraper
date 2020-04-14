from requests import get
from bs4 import BeautifulSoup


def get_villager_list():
    # The URL of the Animal Crossing Wiki
    wiki_url = "https://animalcrossing.fandom.com"

    # Get the page and parse it with BeautifulSoup
    response = get(wiki_url + "/wiki/Villager_list_(New_Horizons)")
    soup_response = BeautifulSoup(response.text, 'html.parser')

    # Try to locate the specific table containing all the villagers
    villager_table = []
    found = False

    # Check each table
    for table in soup_response.find_all("table"):

        # The head of the "Villager" table has a link to a general "Villagers" page
        for link in table.find_all("a"):
            if "/wiki/Villagers" in link.get("href"):
                villager_table = table
                found = True
                break
            if found:
                break

    # Couldn't locate the table
    if len(villager_table) == 0:
        print("Uh-oh, couldn't locate the table.\n\n" +
              "Maybe the wiki has changed, and broken this scraper.\n" +
              "In any case, please make an issue and I'll try to fix it!")
        exit(0)

    # Only add each link once
    links = []
    for tr in villager_table.find_all("tr"):

        # The first column for each villager is uniquely bolded
        for bolded in tr.find_all("b"):
            for link in bolded.find_all("a"):
                l = link.get("href")
                if l not in links:
                    links.append(l)
