"""
Read a directory containing files with Long_Lat_XXX_Time.png format
and create a JSON with their URLs on Zenodo
"""

import os
import json
import re



INPUT_DIR = "/Users/nbarlow/Desktop/TEST_IMAGES"
BASE_URL = "https://zenodo.org/record/3562542/files/"
REGEX = "([\d\.]+)_([\d\.]+)_[\d]+_([\d]{4}-[\d]{2}-[\d]{2}).png"


output_json = []
for filename in os.listdir(INPUT_DIR):
    url = BASE_URL+filename+"?display=1"
    match = re.search(REGEX, filename)
    if not match:
        print("Could not extract data from filename {}".format(filename))
        continue
    latitude, longitude, date = match.groups()
    this_entry = {
        "image_location": url,
        "image_location_is_url": True,
        "image_latitude": latitude,
        "image_longitude": longitude,
        "image_time": date
        }
    output_json.append(this_entry)

with open("catalogue.json","w") as outfile:
    json.dump(output_json, outfile)
