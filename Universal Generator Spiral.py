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
RAND = random.randrange(0, 240000000000)

# ---------------------------------------------------------------------------
NAME = raw_input('Galaxy Name:')

NUMC = int(raw_input('Number of Globular Clusters other than Central <Default:0>:') or "1")

NUMHUB = int(raw_input('Number of Core Stars <Default:2000>:') or "2000")

NUMDISK = int(raw_input('Number of Disk Stars <Default:4000>:') or "4000")

NUMCLUSA = NUMHUB / 70

NUMCLUS = int(raw_input('Number of Stars in each Cluster <Default:Hub / 70>:') or str(NUMCLUSA))

DISCLUSA = NUMCLUS / 4

DISCLUS = int(raw_input('Distribution of Star Number in each Cluster <Default: Avg/ 4>:') or str(DISCLUSA))

HUBRAD = float(raw_input('Radius of Core <Default:90.0>:') or "90.0")

DISKRAD = float(raw_input('Radius of Disk <Default:45.0>:') or "45.0")

CLUSRADA = NUMCLUS / 5

CLUSRAD = float(raw_input('Radius of each cluster <Default:Star Number / 2>:') or str(CLUSRADA))

DISCLRADA = CLUSRAD / 5

DISCLRAD = float(raw_input('Distribution of Cluster Radius <Default:Avg / 5>:') or str(DISCLRADA))

NUMARMS = int(raw_input('Number of Galactic Arms <Default:3>:') or "3")

ARMROTS = float(raw_input('Tightness of Arm Winding <Default:0.5>:') or "0.5")

ARMWIDTH = float(raw_input('Arm Width in Degrees <Default:65>:') or "65")

MAXHUBZ = float(raw_input('Maximum Depth of Core <Default:16.0>:') or "16.0")

MAXDISKZ = float(raw_input('Maximum Depth of Arms <Default:2.0>:') or "2.0")

FUZZ = float(raw_input('Maximum Outlier Distance from Arms <Default:25.0>:') or "25.0")

PNGSIZE = float(raw_input('X and Y Size of PNG <Default:1200>:') or "1200")

PNGFRAME = float(raw_input('PNG Frame Size <Default:50>:') or "50")

stars = []
clusters = []

star_color_dict = {
    0: (255, 185, 201),
    1: (255, 204, 198),
    2: (255, 204, 198),
    3: (255, 218, 198),
    4: (255, 218, 198),
    5: (255, 219, 178),
    6: (255, 233, 178),
    7: (255, 233, 178),
    8: (255, 233, 178),
    9: (255, 233, 178),
    10: (255, 246, 178),
    11: (255, 253, 178),
    12: (255, 253, 178),
    13: (255, 254, 212),
    14: (255, 254, 212),
    15: (254, 255, 248),
    16: (255, 255, 255),
    17: (236, 255, 255),
    18: (236, 255, 255),
    19: (207, 251, 255),
    20: (207, 251, 255),
    21: (207, 251, 255),
    22: (207, 238, 255),
    23: (165, 196, 255)
}

SHRAD = HUBRAD * 0.1
SCRAD = CLUSRAD * 0.06
SDRAD = DISKRAD * 0.1
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
    if NUMARMS:
        omega = 360.0 / NUMARMS
    else:
        omega = 0.0
    i = 0
    while i < NUMDISK:

        # Choose a random distance from center
        dist = HUBRAD + random.random() * DISKRAD
        distb = dist + random.uniform(0,SDRAD)

        # This is the 'clever' bit, that puts a star at a given distance
        # into an arm: First, it wraps the star round by the number of
        # rotations specified.  By multiplying the distance by the number of
        # rotations the rotation is proportional to the distance from the
        # center, to give curvature
        theta = ((360.0 * ARMROTS * (distb / DISKRAD))

                 # Then move the point further around by a random factor up to
                 # ARMWIDTH
                 + random.random() * ARMWIDTH

                 # Then multiply the angle by a factor of omega, putting the
                 # point into one of the arms
                 # + (omega * random.random() * NUMARMS )
                 + omega * random.randrange(0, NUMARMS)

                 # Then add a further random factor, 'fuzzin' the edge of the arms
                 + random.random() * FUZZ * 2.0 - FUZZ
                 # + random.randrange( -FUZZ, FUZZ )
                 )

        # Convert to cartesian
        #def cartesian_convert
        x = math.cos(theta * math.pi / 180.0) * distb
        y = math.sin(theta * math.pi / 180.0) * distb
        z = random.random() * MAXDISKZ * 2.0 - MAXDISKZ
        
        # Replaces the if/elif logic with a simple lookup. Faster and
        # and easier to read.
        scol = star_color_dict[random.randrange(0,23)]

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
        scol = star_color_dict[random.randrange(0,23)]

        # Add star to the stars array
        stars.append((x, y, z, scol))

        # Process next star
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
                scol = star_color_dict[random.randrange(0,23)]
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
drawToPNG("spiralgalaxy" + str(RAND) + "-" + str(NAME) + ".png")

# Create the galaxy's data galaxy.txt
with open("spiralgalaxy" + str(RAND) + "-" + str(NAME) + ".txt", "w") as text_file:
    text_file.write("Galaxy Number: {}".format(RAND)
                   )
    text_file.write("Galaxy Name: {}".format(NAME)
                   )
    text_file.write("Number of Clusters: {}".format(NUMC)
                   )
    text_file.write("Hub Stars: {}".format(NUMHUB)
                   )
    text_file.write("Number of Stars per Cluster: {}".format(NUMCLUS)
                   )
    text_file.write("Star Number Distribution per Cluster: {}".format(DISCLUS)
                   )
    text_file.write("Disk Stars: {}".format(NUMDISK)
                   )
    text_file.write("Hub Radius: {}".format(HUBRAD)
                   )
    text_file.write("Cluster Radius: {}".format(CLUSRAD)
                   )
    text_file.write("Cluster Radius Distribution: {}".format(DISCLRAD)
                   )
    text_file.write("Disk Radius: {}".format(DISKRAD)
                   )
    text_file.write("Arm Number: {}".format(NUMARMS)
                   )
    text_file.write("Arm Rotation: {}".format(ARMROTS)
                   )
    text_file.write("Arm Width: {}".format(ARMWIDTH)
                   )
    text_file.write("Hub Maximum Depth: {}".format(MAXHUBZ))
    
    text_file.write("Disk Maximum Depth: {}".format(MAXDISKZ)
                   )
    text_file.write("Maximum Outlier Distance: {}".format(FUZZ)
                   )
    text_file.write("Image Size: {}".format(PNGSIZE)
                   )
    text_file.write("Frame Size: {}".format(PNGFRAME)
                   )