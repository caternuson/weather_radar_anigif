#!/usr/bin/env python3

from PIL import Image
import requests

# --| User Config |---------------------------------------------------

# Filename(s)
BASE_FILE = None #"base.png"
OUT_FILE = "out.gif"

# Radar images
LAT = 47.42  # latitude
LON = -122.59  # longitude
ZOOM = 6  # zoom level 0 (least) to (20) most
SIZE = 512  # 256 or 512
COLOR = 4  # 0 to 8 see: https://www.rainviewer.com/api/color-schemes.html
SMOOTH = 0  # blur(1) or not (0) radar data
SNOW = 1  # display(1) or not (0) snow

# GIF creation
LOOP = 0  # 0 = forever, N = number of loops
DURATION = 100  # ms per frame

# --| User Config |---------------------------------------------------

API_URL = "https://api.rainviewer.com/public/weather-maps.json"
resp = requests.get(API_URL).json()
HOST = resp["host"]

print("Getting images...")
radar_images = []
if BASE_FILE:
    radar_images.append(Image.open(BASE_FILE))
for past in resp["radar"]["past"]:
    img_url = HOST + past["path"]
    img_url += "/{}/{}/{}/{}/{}/{}_{}.png".format(
        SIZE, ZOOM, LAT, LON, COLOR, SMOOTH, SNOW
    )
    print(past["time"], img_url)
    img = Image.open(requests.get(img_url, stream=True).raw)
    radar_images.append(img)

print("Saving GIF to", OUT_FILE)
if BASE_FILE:
    DISPOSAL = (1,) + (3,)*len(radar_images)
else:
    DISPOSAL = 2
radar_images[0].save(
    OUT_FILE, save_all=True, append_images=radar_images, disposal=DISPOSAL, loop=LOOP, duration=DURATION
)

print("DONE.")
