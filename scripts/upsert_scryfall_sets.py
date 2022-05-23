import requests

r = requests.get('https://api.scryfall.com/sets')
sets = r.json()

if sets["object"] != "list":
    print("Unexpected result from scryfall")
    exit()

for set in sets["data"]:
    # Upsert into DB
    print(set["name"])