#
# This script generates a 3D galaxy from a number of parameters and stores
# it in an array. You can modify this script to store the data in a database
# or whatever your purpose is. THIS script uses the data only to generate a
# PNG with a 2D view from top of the galaxy.
#
# The algorithm used to generate the galaxy is borrowed from Ben Motz
# <motzb@hotmail.com>. The original C source code for DOS (including a 3D
# viewer) can be downloaded here:
#
# http://bits.bristol.ac.uk/motz/tep/galaxy.html
#
# Unfortunately, the original python code has been lost to time and a lack of wanting-to- search-through-several-hundred-webpages-for-one-webarchive-page. Sorry, original python guy.
#
# A fair portion of the revisions and code is from /u/_Foxtrot_ on reddit. They are much better with the python-fu than I!
#

from PIL import Image
from PIL import ImageDraw
import random
import math
import sys

# Generation parameters:

# raw_input the user's desired values
# Background color of the created PNG
PNGBGCOLOR = (0, 0, 0)

# Quick Filename
RAND = random.randrange(0, 108000000000)

# ---------------------------------------------------------------------------
NAME = raw_input('Galaxy Name:')

NUMC = int(raw_input('Number of Globular Clusters other than Central <Default:0>:') or "1")

NUMSTR = int(raw_input('Number of Stars <Default:2000>:') or "2000")

NUMCLUSA = NUMSTR / 70

NUMCLUS = int(raw_input('Number of Stars in each Cluster <Default:Hub / 70>:') or str(NUMCLUSA))

DISCLUSA = NUMCLUS / 4

DISCLUS = int(raw_input('Distribution of Star Number in each Cluster <Default: Avg/ 4>:') or str(DISCLUSA))

GALX = float(raw_input('X Length of Galaxy <Default:90.0>:') or "90.0")

GALY = float(raw_input('Y Length of Galaxy <Default:90.0:') or "90.0")

GALZ = float(raw_input('Maximum Depth of Galaxy <Default:16.0>:') or "16.0")

CLUSRADA = GALX / 12

CLUSRAD = float(raw_input('Radius of each cluster <Default:Hub / 12>:') or str(CLUSRADA))

DISCLRADA = CLUSRAD / 5

DISCLRAD = float(raw_input('Distribution of Cluster Radius <Default:Avg / 5>:') or str(DISCLRADA))

PNGSIZE = float(raw_input('X and Y Size of PNG <Default:1200>:') or "1200")

PNGFRAME = float(raw_input('PNG Frame Size <Default:50>:') or "50")

stars = []
clusters = []

star_color_dict = {
    0: (229, 30, 30),
    1: (203, 30, 26),
    2: (181, 18, 6),
    3: (200, 39, 13),
    4: (200, 63, 21),
    5: (222, 75, 10),
    6: (222, 102, 10),
    7: (222, 137, 10),
    8: (212, 178, 42),
    9: (210, 188, 38),
    10: (217, 207, 66),
    11: (217, 207, 66),
    12: (222, 226, 125),
    13: (222, 226, 125),
    14: (255, 255, 253),
    15: (255, 255, 255),
    16: (253, 255, 255),
    17: (222, 243, 255),
    18: (222, 243, 255),
    19: (140, 176, 225)
}

SGX = GALX * 0.1
SGY = GALY * 0.1
SCRAD = CLUSRAD * 0.06
NUMCLUSA = NUMCLUS - DISCLUS
NUMCLUSB = NUMCLUS + DISCLUS
CLUSRADA = CLUSRAD - DISCLRAD
CLUSRADB = CLUSRAD + DISCLRAD
NUMCB = NUMC + 1

def generateClusters():
    c = 0
    cx = 0
    cy = 0
    cz = 0
    rad = random.uniform(CLUSRADA, CLUSRADB)
    num = random.uniform(NUMCLUSA, NUMCLUSB)
    clusters.append((cx, cy, cz, rad, num))
    c = 1
    while c < NUMCB:
        # random distance from centre
        dist = random.uniform(CLUSRAD, GALX)
        # any rotation- clusters can be anywhere
        theta = random.random() * 360
        cx = math.cos(theta * math.pi / 180.0) * dist
        cy = math.sin(theta * math.pi / 180.0) * dist
        cz = random.random() * GALZ * 2.0 - GALZ
        rad = random.uniform(CLUSRADA, CLUSRADB)
        num = random.uniform(NUMCLUSA, NUMCLUSB)
        # add cluster to clusters array
        clusters.append((cx, cy, cz, rad, num))
        # process next
        c = c+1
        sran = 0
        cran = 0

def generateStars():

    # Now generate the Hub. This places a point on or under the curve
    # maxHubZ - s d^2 where s is a scale factor calculated so that z = 0 is
    # at maxHubR (s = maxHubZ / maxHubR^2) AND so that minimum hub Z is at
    # maximum disk Z. (Avoids edge of hub being below edge of disk)

    scale = GALZ / (GALX * GALY)
    i = 0
    while i < NUMSTR:
        
        # Choose a random distance from center
        distX = random.random() * GALX
        distY = random.random() * GALY
        distXb = distX + random.uniform(0,SGX)
        distYb = distY + random.uniform(0,SGY)
        
        # Any rotation (points are not on arms)
        theta = random.random() * 360

        # Convert to cartesian
        x = math.cos(theta * math.pi / 180.0) * distXb
        y = math.sin(theta * math.pi / 180.0) * distYb
        z = (random.random() * 2 - 1) * (GALZ - scale * distXb * distYb)
        
        # Replaces the if/elif logic with a simple lookup. Faster and
        # and easier to read.
        scol = star_color_dict[random.randrange(0,19)]

        # Add star to the stars array
        stars.append((x, y, z, scol))

        # Process next star
        i = i + 1
        sran = 0
        
    c = 0
    while c < NUMCB:
        for (cx, cy, cz, rad, num) in clusters:    
            scale = rad / (rad * rad)
            i = 0
            while i < num:
                dist = random.uniform(-rad,rad)
                distb = dist + random.uniform(0,SCRAD)
                theta = random.random() * 360
                # Cartesian!
                x = cx + (math.cos(theta * math.pi / 180) * distb)
                y = cy + (math.sin(theta * math.pi / 180) * distb)
                z = (random.random() * 2 - 1) * ((cz + rad) - scale * distb * distb)
                scol = star_color_dict[random.randrange(0,19)]
                stars.append((x, y, z, scol))
                i = i + 1
                sran = 0
        c = c+1
    
    


def drawToPNG(filename):
    image = Image.new("RGB", (int(PNGSIZE), int(PNGSIZE)), PNGBGCOLOR)
    draw = ImageDraw.Draw(image)

    # Find maximal star distance
    max = 0
    for (x, y, z, scol) in stars:
        if abs(x) > max: max = x
        if abs(y) > max: max = y
        if abs(z) > max: max = z
        
    # Calculate zoom factor to fit the galaxy to the PNG size
    factor = float(PNGSIZE - PNGFRAME * 2) / (max * 2)
    for (x, y, z, scol) in stars:
        sx = factor * x + PNGSIZE / 2
        sy = factor * y + PNGSIZE / 2
        draw.point((sx, sy), fill=scol)

    # Save the PNG
    image.save(filename)
    print filename


# Generate the galaxy
generateClusters()
generateStars()

# Save the galaxy as PNG to galaxy.png
drawToPNG("ellipticalgalaxy" + str(RAND) + "-" + str(NAME) + ".png")

# Create the galaxy's data galaxy.txt
with open("ellipticalgalaxy" + str(RAND) + "-" + str(NAME) + ".txt", "w") as text_file:
    text_file.write("Galaxy Number: {}".format(RAND))
    text_file.write("Galaxy Name: {}".format(NAME))
    text_file.write("Number of Clusters: {}".format(NUMC))
    text_file.write("Stars: {}".format(NUMSTR))
    text_file.write("Number of Stars per Cluster {}".format(NUMCLUS))
    text_file.write("Star Number Distribution per Cluster {}".format(DISCLUS))
    text_file.write("Galaxy X Length: {}".format(GALX))
    text_file.write("Galaxy Y Length: {}".format(GALY))
    text_file.write("Galaxy Z Length: {}".format(GALZ))
    text_file.write("Cluster Radius: {}".format(CLUSRAD))
    text_file.write("Cluster Radius Distribution: {}".format(DISCLRAD))
    text_file.write("Image Size: {}".format(PNGSIZE))
    text_file.write("Frame Size: {}".format(PNGFRAME))