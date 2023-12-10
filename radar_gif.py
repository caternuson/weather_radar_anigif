#!/usr/bin/env python3

from PIL import Image
import requests

# --| User Config |---------------------------------------------------
<<<<<<< HEAD
# Filenames
BASE_FILE = None        # filename or `None` to use color
BASE_COLOR = (0, 0, 0)  # color RGB tuple
RAW_FILE = "raw.gif"    # original size from rainview API
SCALED_FILE = "out.gif" # scaled
PIXEL_FILE="pxl.gif"    # pixelated
=======

# Filename(s)
BASE_FILE = None #"base.png"
OUT_FILE = "out.gif"
>>>>>>> 6b423c1a286ce1ebc6735679d77ea5f01a8c05bb

# Radar images
API_URL = "https://api.rainviewer.com/public/weather-maps.json"
LAT = 47.42         # latitude
LON = -122.59       # longitude
ZOOM = 8            # zoom level 0 (least) to (20) most
SIZE = 256          # 256 or 512
COLOR = 2           # 0 to 8 see: https://www.rainviewer.com/api/color-schemes.html
SMOOTH = 0          # 0=no blur, 1=blur
SNOW = 1            # 0=no snow, 1=show snow

# GIF creation
ALPHA = 255         # radar transparency (0=clear to 255=solid)
WIDTH = 64          # width in pixels
HEIGHT = 64         # height in pixels
LOOP = 0            # 0=forever, N=number of loops
DURATION = 200      # ms per frame
# --| User Config |---------------------------------------------------


# base image
if BASE_FILE:
    base_image = Image.open(BASE_FILE).convert("RGBA")
else:
    base_image = Image.new("RGBA", (SIZE, SIZE))
    if BASE_COLOR:
        base_image.paste(BASE_COLOR, (0, 0) + base_image.size)

# radar images
print("Getting images...")

radar_images = []

resp = requests.get(API_URL).json()

for past in resp["radar"]["past"]:
    img_url = resp["host"] + past["path"]
    img_url += "/{}/{}/{}/{}/{}/{}_{}.png".format(
        SIZE, ZOOM, LAT, LON, COLOR, SMOOTH, SNOW
    )
    print(past["time"], img_url)
    img = Image.open(requests.get(img_url, stream=True).raw).convert("RGBA")
    img.putalpha(img.getchannel('A').point(lambda i: ALPHA if i>0 else 0))
    radar_images.append(img)

# blend 'em together, like colby, swiss, n chedduh
print("Blenderfyingification...")
frame_images = [
    Image.alpha_composite(base_image, img) for img in radar_images
]

scaled_images = [
    img.resize((WIDTH, HEIGHT)) for img in frame_images
]

pixelated_images = [
    img.resize((SIZE, SIZE), Image.Resampling.NEAREST) for img in scaled_images
]

# save
print("Saving GIFs...")

frame_images[0].save(
    RAW_FILE, save_all=True, append_images=frame_images, disposal=2, loop=LOOP, duration=DURATION
)
scaled_images[0].save(
    SCALED_FILE, save_all=True, append_images=scaled_images, disposal=2, loop=LOOP, duration=DURATION
)
pixelated_images[0].save(
    PIXEL_FILE, save_all=True, append_images=pixelated_images, disposal=2, loop=LOOP, duration=DURATION
)

print("DONE.")
