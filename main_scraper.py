import json
from os import mkdir

from get_villager_list import get_villager_list
from get_villager_data import get_villager_data

# Get our villages

print("Getting the list of villagers to scrape...", end="")
villager_list = get_villager_list()

# Couldn't locate the table
if len(villager_list) == 0:
    print("\nUh-oh, couldn't locate the table.\n\n" +
          "Maybe the wiki has changed, and broken this scraper.\n" +
          "In any case, please make an issue and I'll try to fix it!")
    exit(0)

print("Done")

# Create directory to store images
try:
    mkdir("villager-data")
    print("\nCreated directory (villager-data) for villager data")

    mkdir("villager-data/images")
    print("Created directory (villager-data/images) for villager images\n")
except FileExistsError:
    print("\nDirectory already exists for villager data.\n" +
          "Delete it and try again, if you want to re-download the images.\n")

# Get the data for each villager
total_villager_data = {}
for villager in villager_list:

    villager_local_name = villager.replace("/wiki/",  "")

    print("Getting data on", villager_local_name + "...", end="")
    villager_data = get_villager_data(villager_local_name)
    print("Done")

    total_villager_data[villager_local_name] = villager_data

print("\nSaving villager JSON data...")
with open("villager-data/villager-data.json", "w") as villager_data_file:
    json.dump(total_villager_data, villager_data_file, indent=4)
print("Done")
