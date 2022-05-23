import requests
from clint.textui import progress

r = requests.get('https://api.scryfall.com/bulk-data')
data = r.json()

bulk_data = None
if data["object"] == "list":
    for d in data["data"]:
        if d["type"] == "default_cards":
            bulk_data = d

if bulk_data is None:
    print("Could not find proper data set for bulk import")
    exit()


r = requests.get(bulk_data["download_uri"], stream=True)
file_name = "cards-default.json"
with open(file_name, "wb") as f:
    total_length = int(r.headers.get('content-length'))

    for chunk in progress.bar(r.iter_content(chunk_size=4096), expected_size=(total_length/4096) + 1):
        if chunk:
            f.write(chunk)
            f.flush()