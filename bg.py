import math
import json
import concurrent
from concurrent import futures
from colorthief import ColorThief
from os import listdir, rename
from os.path import isfile, join, getmtime
from random import randint

IMG_DIR = "C:\\Users\\Alex\\Documents\\GitHub\\hue_poll\\images"
COLOR_COUNT = 3
QUALITY = 2
NUM_PROCESSES = 8
EXTRACTED_SUFFIX = ".palette" + str(COLOR_COUNT) + str(QUALITY) + ".jpg"

def colordist(e1, e2):
    rmean = math.floor(( e1[0] + e2[0] ) / 2)
    r = e1[0] - e2[0]
    g = e1[1] - e2[1]
    b = e1[2] - e2[2]
    return math.sqrt((((512+rmean)*r*r)>>8) + 4*g*g + (((767-rmean)*b*b)>>8))

def extractAndRename(src):
    color_thief = ColorThief(join(IMG_DIR, src))
    # get the dominant color
    palette = color_thief.get_palette(color_count=COLOR_COUNT, quality=QUALITY)
    palette = [palette[0], palette[1], palette[2]]
    palette_str = json.dumps(palette)
    dst = palette_str + EXTRACTED_SUFFIX
    try:
        rename(join(IMG_DIR, src), join(IMG_DIR, dst))
    except WindowsError:
        print('failed to rename: ' + join(IMG_DIR, src) + " to " + dst)

def processImages():
    images = [f for f in listdir(IMG_DIR) if ((f.endswith(".jpg") or f.endswith(".jpeg")) and not f.endswith(EXTRACTED_SUFFIX))]
    executor = concurrent.futures.ProcessPoolExecutor(NUM_PROCESSES)
    futures = [executor.submit(extractAndRename, f) for f in images]
    concurrent.futures.wait(futures)
    executor.shutdown()

def getClosestImg(rgb):
    dist = [[9999, "no img"]]
    images = [f for f in listdir(IMG_DIR) if f.endswith(EXTRACTED_SUFFIX)]
    for image in images:
        json_str = image.replace(EXTRACTED_SUFFIX, '')
        palette = json.loads(json_str)
        new = min(colordist(palette[0], rgb), (colordist(palette[1], rgb) * 1.5), (colordist(palette[2], rgb) * 2))
        if new < dist[-1][0]:
            dist.append([new, image])
    if dist[-1][0] is 9999:
        return None
    return join(IMG_DIR, dist[-1 * randint(1, min(30, len(dist) - 1))][1])
    
