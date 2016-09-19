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

HSB = int(raw_input('Hub Size Bracket <0 = 1-100, 1 = 100-1000, 2 = 1000-100000, 3 = 100000-1000000, 4 = 1000000-2000000>:'))

NUMC = (random.randint(0,12))

if HSB == 0: NUMHUB = random.randrange(1, 100)
elif HSB == 1: NUMHUB = random.randrange(100, 1000)
elif HSB == 2: NUMHUB = random.randrange(1000, 100000)
elif HSB == 3: NUMHUB = random.randrange(100000, 1000000)
elif HSB == 4: NUMHUB = random.randrange(1000000, 2000000)

print NUMHUB

NUMINT = int((random.uniform(0.01,0.8)) * NUMHUB)

NUMDISK = int((random.uniform(0.5,4)) * NUMHUB)

NUMCLUS = NUMHUB / 70

DISCLUS = NUMCLUS / 4

HUBRAD = int(NUMHUB / (random.randrange(8,20)))

INTRAD = int((random.uniform(0.3,2)) * HUBRAD)

DISKRAD = int(NUMDISK / (random.randrange(4,18)))

CLUSRAD = NUMCLUS / 5

DISCLRAD = CLUSRAD / 5

NUMARMS = random.randint(0,12)

ARMROTS = random.uniform(0.2,2)

if NUMARMS: ARMWIDTH = (360.0 / NUMARMS) / 1.5
else: ARMWIDTH = 0

MAXHUBZ = int(HUBRAD / (random.uniform(5,1)))

MAXINTZ = MAXHUBZ / 2

MAXDISKZ = int(DISKRAD / (random.uniform(1000,8)))

FUZZ = ARMWIDTH / 4

PNGSIZEA = HUBRAD / 5

PNGFRAMEA = PNGSIZEA / 10

PNGSIZE = float(raw_input('X and Y Size of PNG <Default:Bad Idea>:') or str(PNGSIZEA))

PNGFRAME = float(raw_input('PNG Frame Size <Default:Bad Idea>:') or str(PNGFRAMEA))

stars = []
clusters = []

disstar_color_dict = {
    0: (229, 30, 30),
    1: (203, 30, 26),
    2: (181, 18, 6),
    3: (200, 39, 13),
    4: (200, 63, 21),
    5: (222, 137, 10),
    6: (212, 178, 42),
    7: (210, 188, 38),
    8: (217, 207, 66),
    9: (222, 226, 125),
    10: (222, 226, 160),
    11: (255, 255, 253),
    12: (255, 255, 255),
    13: (253, 255, 255),
    14: (250, 255, 255),
    15: (222, 243, 255),
    16: (222, 243, 255),
    17: (230, 243, 255),
    18: (140, 176, 255),
    19: (140, 176, 225)
}

censtar_color_dict = {
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

SHRAD = HUBRAD * 0.1
DRAD = HUBRAD + INTRAD
SDRAD = DISKRAD * 0.1
SIRAD = INTRAD * 0.1
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
        dist = random.uniform(CLUSRAD, (HUBRAD+DISKRAD))
        # any rotation- clusters can be anywhere
        theta = random.random() * 360
        cx = math.cos(theta * math.pi / 180.0) * dist
        cy = math.sin(theta * math.pi / 180.0) * dist
        cz = random.random() * MAXHUBZ * 2.0 - MAXHUBZ
        rad = random.uniform(CLUSRADA, CLUSRADB)
        num = random.uniform(NUMCLUSA, NUMCLUSB)
        # add cluster to clusters array
        clusters.append((cx, cy, cz, rad, num))
        # process next
        c = c+1
        sran = 0
        cran = 0

def generateStars():
    # omega is the separation (in degrees) between each arm
    # Prevent div by zero error:
    omega = 30.0
    
    i = 0
    while i < NUMDISK:

        # Choose a random distance from center
        dist = DRAD + random.random() * DISKRAD
        distb = dist + random.uniform(0,SDRAD)

        # This is the 'clever' bit, that puts a star at a given distance
        # into an arm: First, it wraps the star round by the number of
        # rotations specified.  By multiplying the distance by the number of
        # rotations the rotation is proportional to the distance from the
        # center, to give curvature
        theta = ((360.0 * (distb / DISKRAD))

                 # Then move the point further around by a random factor up to
                 # ARMWIDTH
                 + random.random() * 65

                 # Then multiply the angle by a factor of omega, putting the
                 # point into one of the arms
                 # + (omega * random.random() * NUMARMS )
                 + omega * random.randrange(0, 12)

                 # Then add a further random factor, 'fuzzin' the edge of the arms
                 + random.random() * 15 * 2.0 - 15
                 # + random.randrange( -FUZZ, FUZZ )
                 )

        # Convert to cartesian
        #def cartesian_convert
        x = math.cos(theta * math.pi / 180.0) * distb
        y = math.sin(theta * math.pi / 180.0) * distb
        z = random.random() * MAXDISKZ * 2.0 - MAXDISKZ
        
        # Replaces the if/elif logic with a simple lookup. Faster and
        # and easier to read.
        scol = disstar_color_dict[random.randrange(0,19)]

        # Add star to the stars array
        stars.append((x, y, z, scol))

        # Process next star
        i = i + 1
        sran = 0

    # Now generate the Hub. This places a point on or under the curve
    # maxHubZ - s d^2 where s is a scale factor calculated so that z = 0 is
    # at maxHubR (s = maxHubZ / maxHubR^2) AND so that minimum hub Z is at
    # maximum disk Z. (Avoids edge of hub being below edge of disk)

    scale = MAXHUBZ / (HUBRAD * HUBRAD)
    i = 0
    while i < NUMHUB:
        
        # Choose a random distance from center
        dist = random.random() * HUBRAD
        distb = dist + random.uniform(0,SHRAD)
        
        # Any rotation (points are not on arms)
        theta = random.random() * 360

        # Convert to cartesian
        x = math.cos(theta * math.pi / 180.0) * distb
        y = math.sin(theta * math.pi / 180.0) * distb
        z = (random.random() * 2 - 1) * (MAXHUBZ - scale * distb * distb)
        
        # Replaces the if/elif logic with a simple lookup. Faster and
        # and easier to read.
        scol = censtar_color_dict[random.randrange(0,19)]

        # Add star to the stars array
        stars.append((x, y, z, scol))

        # Process next star
        i = i + 1
        sran = 0
        
    scale = MAXINTZ / (DRAD * DRAD)
    i = 0
    while i < NUMINT:
        
        dist = HUBRAD + random.random() * INTRAD
        distb = dist + random.uniform(0,SIRAD)
        
        theta = random.random() * 360
        
        x = math.cos(theta * math.pi / 180.0) * distb
        y = math.sin(theta * math.pi / 180.0) * distb
        z = (random.random() * 2 - 1) * (MAXINTZ - scale * distb * distb)
        
        scol = censtar_color_dict[random.randrange(0,19)]
        
        stars.append((x, y, z, scol))
        
        i = i + 1
        sran = 0
        
    # Generate clusters and their stars.
    
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
                scol = censtar_color_dict[random.randrange(0,19)]
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
drawToPNG("ringgalaxy" + str(RAND) + "-" + str(NAME) + ".png")

# Create the galaxy's data galaxy.txt
with open("ringgalaxy" + str(RAND) + "-" + str(NAME) + ".txt", "w") as text_file:
    text_file.write("Galaxy Number: {}".format(RAND))
    text_file.write("Galaxy Name: {}".format(NAME))
    text_file.write("Number of Clusters: {}".format(NUMC))
    text_file.write("Hub Stars: {}".format(NUMHUB))
    text_file.write("Number of Stars per Cluster {}".format(NUMCLUS))
    text_file.write("Star Number Distribution per Cluster {}".format(DISCLUS))
    text_file.write("Intermediate Stars: {}".format(NUMINT))
    text_file.write("Disk Stars: {}".format(NUMDISK))
    text_file.write("Hub Radius: {}".format(HUBRAD))
    text_file.write("Cluster Radius: {}".format(CLUSRAD))
    text_file.write("Cluster Radius Distribution: {}".format(DISCLRAD))
    text_file.write("Intermediate Area Radius: {}".format(INTRAD))
    text_file.write("Disk Radius: {}".format(DISKRAD))
    text_file.write("Hub Maximum Depth: {}".format(MAXHUBZ))
    text_file.write("Disk Maximum Depth: {}".format(MAXDISKZ))
    text_file.write("Intermediate Area Depth: {}".format(MAXINTZ))
    text_file.write("Disk Maximum Depth: {}".format(MAXDISKZ))
    text_file.write("Image Size: {}".format(PNGSIZE))
    text_file.write("Frame Size: {}".format(PNGFRAME))