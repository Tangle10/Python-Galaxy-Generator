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
PNGCOLOR = (255, 255, 255)
PNGBGCOLOR = (0, 0, 0)

# Quick Filename
RAND = random.randrange(0, 2000000000000)

# ---------------------------------------------------------------------------
NAME = raw_input('Galaxy Name:')

PSB = int(raw_input('PNG SIZE BRACKET <0 = 50-100, 1 = 200-400, 2 = 400-800, 3 = 800-1200, 4 = 1200-2500, 5 = 2500-5000, 6 = 5000-7500, 7 = 7500-8000, 8 = 8000-9000, 9 = 9000-12000>:'))

GAL = int(raw_input('GALAXY TYPE <0 = SPIRAL, 1 = RING, 2 = LENTICULAR WITH HUB, 3 = ELLIPTICAL, 4 = LENTICULAR WITHOUT HUB, 5 = STARFIELD'))

if PSB == 0:
    PNGSIZE = int(random.randrange(50,200))
    PNGFRAME = int(random.randrange(5,10))
    NUMC = 0
    
elif PSB == 1:
    PNGSIZE = int(random.randrange(200,400))
    PNGFRAME = int(random.randrange(10,20))
    NUMC = (random.randint(0,1))

elif PSB == 2:
    PNGSIZE = int(random.randrange(400,800))
    PNGFRAME = int(random.randrange(20,40))
    NUMC = (random.randint(0,2))
    
elif PSB == 3:
    PNGSIZE = int(random.randrange(800,1200))
    PNGFRAME = int(random.randrange(40,50))
    NUMC = (random.randint(0,3))
    
elif PSB == 4:
    PNGSIZE = int(random.randrange(1200,2500))
    PNGFRAME = int(random.randrange(50,75))
    NUMC = (random.randint(0,4))
    
elif PSB == 5:
    PNGSIZE = int(random.randrange(2500,5000))
    PNGFRAME = int(random.randrange(75,100))
    NUMC = (random.randint(0,6))
    
elif PSB == 3:
    PNGSIZE = int(random.randrange(5000,7500))
    PNGFRAME = int(random.randrange(100,125))
    NUMC = (random.randint(0,8))
    
elif PSB == 3:
    PNGSIZE = int(random.randrange(7500,8000))
    PNGFRAME = int(random.randrange(125,130))
    NUMC = (random.randint(0,9))
    
elif PSB == 3:
    PNGSIZE = int(random.randrange(8000,9000))
    PNGFRAME = int(random.randrange(130,140))
    NUMC = (random.randint(0,10))
    
elif PSB == 3:
    PNGSIZE = int(random.randrange(9000,12000))
    PNGFRAME = int(random.randrange(140,200))
    NUMC = (random.randint(0,20))
    
    
PNGACT = PNGSIZE - PNGFRAME  
NUMS1 = PNGACT*PNGACT
NUMS2 = int(NUMS1 / 7)
NUMS3 = int(NUMS1 / 300)
NUMS = random.randrange(NUMS2, NUMS3)

print NUMS

if GAL <= 3:
    NUMHUB = int((random.uniform(0.2,1)) * NUMS)
    
else NUMHUB = 0

if GAL <= 1:
    NUMDISK = int((random.uniform(0.2,1.2)) * NUMS)
    
else NUMHUB = 0

NUMMID = int((random.uniform(0.2,.8)) * NUMS)
NUMG = int(NUMHUB + NUMMID + NUMDISK / 1000)

NUMFULL = NUMHUB + NUMMID + NUMDISK + NUMG

print NUMFULL

NUMCLUS = NUMFULL / 70

DISCLUS = NUMCLUS / 4

HUBRAD = int(NUMHUB / (random.randrange(8,20)))

if GAL == 3:
    HUBRADX = int(HUBRAD * random.randrange(0.1,1.2))
    HUBRADY = int(HUBRAD * random.randrange(0.1,1.2))
else: 
    HUBRADX = HUBRAD
    HUBRADY = HUBRAD

DISKRAD = int(NUMDISK / (random.randrange(4,18)))

if GAL == 1:
    GALRAD = HUBRAD + HUBRAD + DISKRAD
    
else: GALRAD = HUBRAD + DISKRAD

CLUSRAD = NUMCLUS / 5

DISCLRAD = CLUSRAD / 5

NUMARMS = random.randint(0,12)

ARMROTS = random.uniform(0.2,2)

if NUMARMS: ARMWIDTH = (360.0 / NUMARMS) / 1.5
else: ARMWIDTH = 0

MAXHUBZ = int(HUBRAD / (random.uniform(5,1)))

MAXDISKZ = int(DISKRAD / (random.uniform(1000,8)))

FUZZ = ARMWIDTH / 4

stars = []
clusters = []

SHRAD = HUBRAD * 0.1
SCRAD = CLUSRAD * 0.06
SDRAD = DISKRAD * 0.1
NUMCLUSA = NUMCLUS - DISCLUS
NUMCLUSB = NUMCLUS + DISCLUS
CLUSRADA = CLUSRAD - DISCLRAD
CLUSRADB = CLUSRAD + DISCLRA
DRAD = HUBRAD + HUBRAD

hubstar_color_dict = {
    0: "ff8080",
    1: "ff8080",
    2: "ff8080",
    3: "ffce7a",
    4: "ffefc3",
    5: "ffffd7",
    6: "ffffd7",
    7: "ffffd7",
    8: "ffffff",
    9: "ffffff", 
}

disstar_color_dict = {
    0: "ffefc3",
    1: "ffffd7",
    2: "ffffd7",
    3: "ffffd7",
    4: "ffffff",
    5: "ffffff",
    6: "ffffff",
    7: "e7ffff",
    8: "e7ffff",
    9: "b5e1ff",  
}

midstar_color_dict = {
    0: "ff8080",
    1: "ffce7a",
    2: "ffefc3",
    3: "ffffd7",
    4: "ffffd7",
    5: "ffffd7",
    6: "ffffff",
    7: "ffffff",
    8: "e7ffff",
    9: "b5e1ff",  
}

def generateClusters():
    c = 0
    cx = 0
    cy = 0
    cz = 0
    rad = random.uniform(CLUSRADA, CLUSRADB)
    num = random.uniform(NUMCLUSA, NUMCLUSB)
    clusters.append((cx, cy, cz, rad, num))
    c = 0
    while c < NUMC:
        # random distance from centre
        dist = random.uniform(CLUSRAD, GALRAD)
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
    if GAL == 0:
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
            SCOL = disstar_color_dict[random.randrange(0,9)]

            # Add star to the stars array
            stars.append((x, y, z, SCOL))

            # Process next star
            i = i + 1
            sran = 0
    
    elif GAL == 1:
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
        SCOL = disstar_color_dict[random.randrange(0,9)]

        # Add star to the stars array
        stars.append((x, y, z, SCOL))


    if GAL <= 3:
        # Now generate the Hub. This places a point on or under the curve
        # maxHubZ - s d^2 where s is a scale factor calculated so that z = 0 is
        # at maxHubR (s = maxHubZ / maxHubR^2) AND so that minimum hub Z is at
        # maximum disk Z. (Avoids edge of hub being below edge of disk)

        scale = MAXHUBZ / (HUBRADX * HUBRADY)
        i = 0
        while i < NUMHUB:
        
            # Choose a random distance from center
            dist = random.random() * HUBRAD
            distb = dist + random.uniform(0,SHRAD)
        
            # Any rotation (points are not on arms)
            theta = random.random() * 360

            # Convert to cartesian
            x = math.cos(theta * math.pi / 180.0) * ((random.random() * HUBRADX) + random.uniform(0,SHRAD))
            y = math.sin(theta * math.pi / 180.0) * ((random.random() * HUBRADY) + random.uniform(0,SHRAD))
            z = (random.random() * 2 - 1) * (MAXHUBZ - scale * distb * distb)
            SCOL = hubstar_color_dict[random.randrange(0,9)]

            # Add star to the stars array
            stars.append((x, y, z, SCOL))

            # Process next star
            i = i + 1
            sran = 0
            
    if GAL <= 4:
        scale = GALRAD
        i = 0
        while i < NUMMID:
            # Choose a random distance from center
            dist = random.random() * GALRAD
        
            # Any rotation (points are not on arms)
            theta = random.random() * 360

            # Convert to cartesian
            x = math.cos(theta * math.pi / 180.0) * dist
            y = math.sin(theta * math.pi / 180.0) * dist
            z = (random.random() * 2 - 1) * (MAXHUBZ - scale * dist * dist)
            SCOL = midstar_color_dict[random.randrange(0,9)]

            # Add star to the stars array
            stars.append((x, y, z, SCOL))

            # Process next star
            i = i + 1
            sran = 0
        
    elif GAL == 5:
        i = 0
        while i < NUMMID:
            x = random.uniform(0,GALRAD)
            y = random.uniform(0,GALRAD)
            z = random.uniform(0,GALRAD)
            SCOL = midstar_color_dict[random.randrange(0,9)]

            # Add star to the stars array
            stars.append((x, y, z, SCOL))

            # Process next star
            i = i + 1
            sran = 0
        
    # Generate clusters and their stars.
    
    i = 0
    while i < NUMG:
        dist = random.uniform(0, GALRAD)
        # any rotation- clusters can be anywhere
        theta = random.random() * 360
        x = math.cos(theta * math.pi / 180.0) * dist
        y = math.sin(theta * math.pi / 180.0) * dist
        z = random.random() * MAXHUBZ * 2.0 - MAXHUBZ
        SCOL = hubstar_color_dict[random.randrange(0,9)]
        rad = random.uniform(CLUSRADA, CLUSRADB)
        num = random.uniform(NUMCLUSA, NUMCLUSB)
        # add cluster to clusters array
        stars.append((x, y, z, SCOL))
        # process next
        i = i+1
        sran = 0
    
    c = 0
    while c < NUMCB:
        for (cx, cy, cz, rad, num) in clusters:    
            if rad: scale = rad / (rad * rad)
            else: scale = 0
            i = 0
            while i < num:
                dist = random.uniform(-rad,rad)
                distb = dist + random.uniform(0,SCRAD)
                theta = random.random() * 360
                # Cartesian!
                x = cx + (math.cos(theta * math.pi / 180) * distb)
                y = cy + (math.sin(theta * math.pi / 180) * distb)
                z = (random.random() * 2 - 1) * ((cz + rad) - scale * distb * distb)
                SCOL = hubstar_color_dict[random.randrange(0,9)]
                stars.append((x, y, z, SCOL))
                i = i + 1
                sran = 0
        c = c+1

def drawToPNG(filename):
    image = Image.new("RGB", (int(PNGSIZE), int(PNGSIZE)), PNGBGCOLOR)
    draw = ImageDraw.Draw(image)

    # Find maximal star distance
    max = 0
    for (x, y, z) in stars:
        if abs(x) > max: max = x
        if abs(y) > max: max = y
        if abs(z) > max: max = z
        
    # Calculate zoom factor to fit the galaxy to the PNG size
    factor = float(PNGSIZE - PNGFRAME * 2) / (max * 2)
    for (x, y, z, SCOL) in stars:
        sx = factor * x + PNGSIZE / 2
        sy = factor * y + PNGSIZE / 2
        draw.point((sx, sy), fill=SCOL)

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
    text_file.write("Galaxy Number: {}".format(RAND))
    text_file.write("Galaxy Name: {}".format(NAME))
    text_file.write("Number of Stars: {}".format((len(stars))))
    text_file.write("Number of Clusters: {}".format((len(clusters))))
    text_file.write("Galaxy Radius: {}".format(GALRAD))
    text_file.write("Image Size: {}".format(PNGSIZE))
    text_file.write("Frame Size: {}".format(PNGFRAME))