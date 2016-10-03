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
import re
from collections import defaultdict

# Generation parameters:

# raw_input the user's desired values
# Background color of the created PNG
PNGBGCOLOR = (0, 0, 0)

# Quick Filename
RAND = random.randrange(0, 240000000000)

# to line 207- made by mewo2:

def choose(lst, exponent=2):
    x = random.random() ** exponent
    return lst[int(x * len(lst))]


# In[98]:

class Language(object):
    def __init__(self, phonemes, syll='CVC', ortho={}, wordlength=(1,4), restricts=[]):
        self.phonemes = {}
        for k, v in phonemes.iteritems():
            v = list(v)
            random.shuffle(v)
            self.phonemes[k] = v
        self.syll = syll
        self.ortho = ortho
        self.wordlength = wordlength
        self.morphemes = defaultdict(list)
        self.allmorphemes = set()
        self.words = defaultdict(list)
        self.restricts = restricts
        self.genitive = self.morpheme('of', 3)
        self.definite = self.morpheme('the', 3)
        self.joiner = random.choice('   -')
        self.minlength = 6
        self.used = []
        self.last_n = []

    def syllable(self):
        while True:
            phones = []
            for s in self.syll:
                if s == '?':
                    if random.random() > 0.5:
                        phones = phones[:-1]
                else:
                    p = choose(self.phonemes[s], 1.5)
                    phones.append(p)
            syll = ''.join(phones)
            for r in self.restricts:
                if re.search(r, syll):
                    break
            else:
                return syll

    def orthosyll(self):
        s = self.syllable()
        o = u""
        for c in s:
            o += self.ortho.get(c, c.lower())
        return o
    
    def morpheme(self, key=None, maxlength=None):
        morphemes = self.morphemes[key]
        n = random.randrange(len(morphemes) + (10 if key is None else 1))
        if n < len(morphemes):
            return morphemes[n]
        for _ in xrange(100):
            s = self.orthosyll()
            if maxlength and len(s) > maxlength:
                continue
            if s not in self.allmorphemes:
                break
        morphemes.append(s)
        self.allmorphemes.add(s)
        return s
    
    def word(self, key=None):
        ws = self.words[key]
        while True:
            n = random.randrange(len(ws) + (3 if key is None else 2))
            if n < len(ws):
                if ws[n] in self.last_n:
                    continue
                self.last_n.append(ws[n])
                self.last_n = self.last_n[-3:]
                return ws[n]
            l = random.randrange(*self.wordlength)
            keys = [key] + [None for _ in xrange(l-1)]
            random.shuffle(keys)
            w = ''.join(self.morpheme(k) for k in keys)
            ws.append(w)
            self.last_n.append(w)
            self.last_n = self.last_n[-3:]
            return w
        
    def name(self, key=None, genitive=0.5, definite=0.1, minlength=5,
            maxlength=12):
        while True:
            if genitive > random.random():
                x = random.random()
                w1 = self.word(key if random.random() < 0.6 
                                   else None).capitalize()
                w2 = self.word(key if random.random() < 0.6 
                                   else None).capitalize()
                if w1 == w2: continue
                if random.random() > 0.5:
                    p = self.joiner.join([w1, self.genitive, w2])
                else:
                    p = self.joiner.join([w1, w2])
            else:
                p = self.word(key).capitalize()
            if random.random() < definite:
                p = self.joiner.join([self.definite, p])
            if not hasattr(self, "used"):
                self.used = []
            for p2 in self.used:
                if p in p2 or p2 in p:
                    break
            else:
                if minlength <= len(p) <= maxlength:
                    self.used.append(p)
                    return p


# In[101]:

vsets = ["AIU", "AEIOU", "AEIOUaei", "AEIOUu", "AIUai", "EOU", "AEIOU@0u"]
csets = ["PTKMNSL", "PTKBDGMNLRSsZzc", "PTKMNH", "HKLMNPW'", 
         "PTKQVSGRMNnLJ", "TKSsDBQgxMNLRWY", "TKDGMNSs",
         "PTKBDGMNzSZcHJW"]
lsets = ["RL", "R", "L", "WY", "RLWY"]
ssets = ["S", "Ss", "SsF"]
fsets = ["MN", "SK", "MNn", 'SsZz']
syllsets = ["CVV?C", "CVC", "CVVC?", "CVC?", "CV", "VC", "CVF", "C?VC", "CVF?", 
            "CL?VC", "CL?VF", "S?CVC", "S?CVF", "S?CVC?", 
             "C?VF", "C?VC?", "C?VF?", "C?L?VC", "VC",
           "CVL?C?", "C?VL?C", "C?VLC?"
           ]
vorthos=[{'a': u'a', 'e': u'e', 'i': u'i', 'u': u'u', '@': u'a', '0': u'o'},
         {'a': u'au', 'e': u'ei', 'i': u'ie', 'u': u'oo', '@': u'ea', '0': u'ou'},
         {'a': u'a', 'e': u'e', 'i': u'y', 'u': u'w', '@': u'a', '0': u'o'},
         {'a': u'aa', 'e': u'ee', 'i': u'ii', 'u': u'uu', '@': u'ai', '0': u'oo'}]
corthos = [{'n': 'ng', 'x': 'kh', 's': 'sh', 'g': 'gh', 'z': 'zh', 'c': 'ch'},
           {'n': u'ny', 'x': 'x', 's': u's', 'g': u'gh', 'z': u'z', 'c': u'c'},
           {'n': u'ng', 'x': 'ch', 's': u'sch', 'g': u'gh', 'z': u'ts', 'c': u'tsch'},
          {'n': u'ng', 'x': 'c', 's': u'ch', 'g': u'gh', 'z': u'j', 'c': u'tch'},
          {'n': u'ng', 'x': 'c', 's': u'x', 'g': u'g', 'z': u'zh', 'c': u'q'}]
restricts = ['Ss', 'sS', 'LR', 'RL', "FS", "Fs", "SS", "ss", r"(.)\1"]


# In[102]:
def get_language():
    while True:
        cset = choose(csets)
        vset = choose(vsets)
        syll = choose(syllsets, 1)
        if len(cset) ** syll.count("C") * len(vset) * syll.count("V") > 30:
            break
    fset = choose([cset, random.choice(fsets), cset + random.choice(fsets)])
    lset = choose(lsets)
    sset = choose(ssets)
    ortho = {"'": u"`"}
    ortho.update(choose(vorthos))
    ortho.update(choose(corthos))
    minlength = random.choice([1,2])
    if len(syll) < 3:
        minlength += 1
    maxlength = random.randrange(minlength+1, 7)

    l = Language(phonemes={'V': vset, 
                           'C': cset, 
                           'L': lset,
                           'F': fset,
                           'S': sset},
                 syll=syll,
                 ortho=ortho,
                restricts=restricts,
                wordlength=(minlength, maxlength))
    return l

def show_language(l):
    print l.phonemes['V'], l.phonemes['C']
    if 'F' in l.syll: print l.phonemes['F'],
    if 'L' in l.syll: print l.phonemes['L'],
    if 'S' in l.syll: print l.phonemes['S'],
    print l.syll
    n = 0
    while n < starnumb:
        bet = (l.name("city"))
        print bet
        wds.append(str(bet))
        n = n+1
    print u', '.join(wds)
    print "* * *"

# ---------------------------------------------------------------------------
NAME = raw_input('Galaxy Name:')

HSB = int(raw_input('Hub Size Bracket <0 = 1-100, 1 = 100-1000, 2 = 1000-100000, 3 = 100000-1000000, 4 = 1000000-2000000>, 5 = 2000000-3200000:'))

NUMC = (random.randint(0,20))

if HSB == 0: NUMHUB = random.randrange(1, 100)
elif HSB == 1: NUMHUB = random.randrange(100, 1000)
elif HSB == 2: NUMHUB = random.randrange(1000, 100000)
elif HSB == 3: NUMHUB = random.randrange(100000, 1000000)
elif HSB == 4: NUMHUB = random.randrange(1000000, 2000000)
elif HSB == 5: NUMHUB = random.randrange(2000000, 3200000)
    
if HSB == 0: empn = 2
elif HSB == 1: empn = 6
elif HSB == 2: empn = 12
elif HSB == 3: empn = 60
elif HSB == 4: empn = 120
elif HSB == 5: empn = 512

starnumpre = floor((NUMHUB + NUMDISK) / empn)
starnumear = int(starnumpre)


print NUMHUB

NUMDISK = int((random.uniform(0.5,4)) * NUMHUB)

NUMCLUS = NUMHUB / 70

DISCLUS = NUMCLUS / 4

HUBRAD = int(NUMHUB / (random.randrange(8,20)))

DISKRAD = int(NUMDISK / (random.randrange(4,18)))

CLUSRAD = NUMCLUS / 5

DISCLRAD = CLUSRAD / 5

NUMARMS = random.randint(0,12)

ARMROTS = random.uniform(0.2,2)

if NUMARMS: ARMWIDTH = (360.0 / NUMARMS) / 1.5
else: ARMWIDTH = 0

MAXHUBZ = int(HUBRAD / (random.uniform(5,1)))

MAXDISKZ = int(DISKRAD / (random.uniform(1000,8)))

FUZZ = ARMWIDTH / 4

PNGSIZEA = HUBRAD / 5

PNGFRAMEA = PNGSIZEA / 10

PNGSIZE = float(raw_input('X and Y Size of PNG <Default:Bad Idea>:') or str(PNGSIZEA))

PNGFRAME = float(raw_input('PNG Frame Size <Default:Bad Idea>:') or str(PNGFRAMEA))

stars = []
clusters = []

speccolor = ["#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
    "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
    "#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
    "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
    "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
    "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
    "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
    "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",
    "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
    "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
    "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
    "#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
    "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
    "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
    "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
    "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58",
    "#7A7BFF", "#D68E01", "#353339", "#78AFA1", "#FEB2C6", "#75797C", "#837393", "#943A4D",
    "#B5F4FF", "#D2DCD5", "#9556BD", "#6A714A", "#001325", "#02525F", "#0AA3F7", "#E98176",
    "#DBD5DD", "#5EBCD1", "#3D4F44", "#7E6405", "#02684E", "#962B75", "#8D8546", "#9695C5",
    "#E773CE", "#D86A78", "#3E89BE", "#CA834E", "#518A87", "#5B113C", "#55813B", "#E704C4",
    "#00005F", "#A97399", "#4B8160", "#59738A", "#FF5DA7", "#F7C9BF", "#643127", "#513A01",
    "#6B94AA", "#51A058", "#A45B02", "#1D1702", "#E20027", "#E7AB63", "#4C6001", "#9C6966",
    "#64547B", "#97979E", "#006A66", "#391406", "#F4D749", "#0045D2", "#006C31", "#DDB6D0",
    "#7C6571", "#9FB2A4", "#00D891", "#15A08A", "#BC65E9", "#FFFFFE", "#C6DC99", "#203B3C",
    "#671190", "#6B3A64", "#F5E1FF", "#FFA0F2", "#CCAA35", "#374527", "#8BB400", "#797868",
    "#C6005A", "#3B000A", "#C86240", "#29607C", "#402334", "#7D5A44", "#CCB87C", "#B88183",
    "#AA5199", "#B5D6C3", "#A38469", "#9F94F0", "#A74571", "#B894A6", "#71BB8C", "#00B433",
    "#789EC9", "#6D80BA", "#953F00", "#5EFF03", "#E4FFFC", "#1BE177", "#BCB1E5", "#76912F",
    "#003109", "#0060CD", "#D20096", "#895563", "#29201D", "#5B3213", "#A76F42", "#89412E",
    "#1A3A2A", "#494B5A", "#A88C85", "#F4ABAA", "#A3F3AB", "#00C6C8", "#EA8B66", "#958A9F",
    "#BDC9D2", "#9FA064", "#BE4700", "#658188", "#83A485", "#453C23", "#47675D", "#3A3F00",
    "#061203", "#DFFB71", "#868E7E", "#98D058", "#6C8F7D", "#D7BFC2", "#3C3E6E", "#D83D66",
    "#2F5D9B", "#6C5E46", "#D25B88", "#5B656C", "#00B57F", "#545C46", "#866097", "#365D25",
    "#252F99", "#00CCFF", "#674E60", "#FC009C", "#92896B", "#1E2324", "#DEC9B2", "#9D4948",
    "#85ABB4", "#342142", "#D09685", "#A4ACAC", "#00FFFF", "#AE9C86", "#742A33", "#0E72C5",
    "#AFD8EC", "#C064B9", "#91028C", "#FEEDBF", "#FFB789", "#9CB8E4", "#AFFFD1", "#2A364C",
    "#4F4A43", "#647095", "#34BBFF", "#807781", "#920003", "#B3A5A7", "#018615", "#F1FFC8",
    "#976F5C", "#FF3BC1", "#FF5F6B", "#077D84", "#F56D93", "#5771DA", "#4E1E2A", "#830055",
    "#02D346", "#BE452D", "#00905E", "#BE0028", "#6E96E3", "#007699", "#FEC96D", "#9C6A7D",
    "#3FA1B8", "#893DE3", "#79B4D6", "#7FD4D9", "#6751BB", "#B28D2D", "#E27A05", "#DD9CB8",
    "#AABC7A", "#980034", "#561A02", "#8F7F00", "#635000", "#CD7DAE", "#8A5E2D", "#FFB3E1",
    "#6B6466", "#C6D300", "#0100E2", "#88EC69", "#8FCCBE", "#21001C", "#511F4D", "#E3F6E3",
    "#FF8EB1", "#6B4F29", "#A37F46", "#6A5950", "#1F2A1A", "#04784D", "#101835", "#E6E0D0",
    "#FF74FE", "#00A45F", "#8F5DF8", "#4B0059", "#412F23", "#D8939E", "#DB9D72", "#604143",
    "#B5BACE", "#989EB7", "#D2C4DB", "#A587AF", "#77D796", "#7F8C94", "#FF9B03", "#555196",
    "#31DDAE", "#74B671", "#802647", "#2A373F", "#014A68", "#696628", "#4C7B6D", "#002C27",
    "#7A4522", "#3B5859", "#E5D381", "#FFF3FF", "#679FA0", "#261300", "#2C5742", "#9131AF",
    "#AF5D88", "#C7706A", "#61AB1F", "#8CF2D4", "#C5D9B8", "#9FFFFB", "#BF45CC", "#493941",
    "#863B60", "#B90076", "#003177", "#C582D2", "#C1B394", "#602B70", "#887868", "#BABFB0",
    "#030012", "#D1ACFE", "#7FDEFE", "#4B5C71", "#A3A097", "#E66D53", "#637B5D", "#92BEA5",
    "#00F8B3", "#BEDDFF", "#3DB5A7", "#DD3248", "#B6E4DE", "#427745", "#598C5A", "#B94C59",
    "#8181D5", "#94888B", "#FED6BD", "#536D31", "#6EFF92", "#E4E8FF", "#20E200", "#FFD0F2",
    "#4C83A1", "#BD7322", "#915C4E", "#8C4787", "#025117", "#A2AA45", "#2D1B21", "#A9DDB0",
    "#FF4F78", "#528500", "#009A2E", "#17FCE4", "#71555A", "#525D82", "#00195A", "#967874",
    "#555558", "#0B212C", "#1E202B", "#EFBFC4", "#6F9755", "#6F7586", "#501D1D", "#372D00",
    "#741D16", "#5EB393", "#B5B400", "#DD4A38", "#363DFF", "#AD6552", "#6635AF", "#836BBA",
    "#98AA7F", "#464836", "#322C3E", "#7CB9BA", "#5B6965", "#707D3D", "#7A001D", "#6E4636",
    "#443A38", "#AE81FF", "#489079", "#897334", "#009087", "#DA713C", "#361618", "#FF6F01",
    "#006679", "#370E77", "#4B3A83", "#C9E2E6", "#C44170", "#FF4526", "#73BE54", "#C4DF72",
    "#ADFF60", "#00447D", "#DCCEC9", "#BD9479", "#656E5B", "#EC5200", "#FF6EC2", "#7A617E",
    "#DDAEA2", "#77837F", "#A53327", "#608EFF", "#B599D7", "#A50149", "#4E0025", "#C9B1A9",
    "#03919A", "#1B2A25", "#E500F1", "#982E0B", "#B67180", "#E05859", "#006039", "#578F9B",
    "#305230", "#CE934C", "#B3C2BE", "#C0BAC0", "#B506D3", "#170C10", "#4C534F", "#224451",
    "#3E4141", "#78726D", "#B6602B", "#200441", "#DDB588", "#497200", "#C5AAB6", "#033C61",
    "#71B2F5", "#A9E088", "#4979B0", "#A2C3DF", "#784149", "#2D2B17", "#3E0E2F", "#57344C",
    "#0091BE", "#E451D1", "#4B4B6A", "#5C011A", "#7C8060", "#FF9491", "#4C325D", "#005C8B",
    "#E5FDA4", "#68D1B6", "#032641", "#140023", "#8683A9", "#CFFF00", "#A72C3E", "#34475A",
    "#B1BB9A", "#B4A04F", "#8D918E", "#A168A6", "#813D3A", "#425218", "#DA8386", "#776133",
    "#563930", "#8498AE", "#90C1D3", "#B5666B", "#9B585E", "#856465", "#AD7C90", "#E2BC00",
    "#E3AAE0", "#B2C2FE", "#FD0039", "#009B75", "#FFF46D", "#E87EAC", "#DFE3E6", "#848590",
    "#AA9297", "#83A193", "#577977", "#3E7158", "#C64289", "#EA0072", "#C4A8CB", "#55C899",
    "#E78FCF", "#004547", "#F6E2E3", "#966716", "#378FDB", "#435E6A", "#DA0004", "#1B000F",
    "#5B9C8F", "#6E2B52", "#011115", "#E3E8C4", "#AE3B85", "#EA1CA9", "#FF9E6B", "#457D8B",
    "#92678B", "#00CDBB", "#9CCC04", "#002E38", "#96C57F", "#CFF6B4", "#492818", "#766E52",
    "#20370E", "#E3D19F", "#2E3C30", "#B2EACE", "#F3BDA4", "#A24E3D", "#976FD9", "#8C9FA8",
    "#7C2B73", "#4E5F37", "#5D5462", "#90956F", "#6AA776", "#DBCBF6", "#DA71FF", "#987C95",
    "#52323C", "#BB3C42", "#584D39", "#4FC15F", "#A2B9C1", "#79DB21", "#1D5958", "#BD744E",
    "#160B00", "#20221A", "#6B8295", "#00E0E4", "#102401", "#1B782A", "#DAA9B5", "#B0415D",
    "#859253", "#97A094", "#06E3C4", "#47688C", "#7C6755", "#075C00", "#7560D5", "#7D9F00",
    "#C36D96", "#4D913E", "#5F4276", "#FCE4C8", "#303052", "#4F381B", "#E5A532", "#706690",
    "#AA9A92", "#237363", "#73013E", "#FF9079", "#A79A74", "#029BDB", "#FF0169", "#C7D2E7",
    "#CA8869", "#80FFCD", "#BB1F69", "#90B0AB", "#7D74A9", "#FCC7DB", "#99375B", "#00AB4D",
    "#ABAED1", "#BE9D91", "#E6E5A7", "#332C22", "#DD587B", "#F5FFF7", "#5D3033", "#6D3800",
    "#FF0020", "#B57BB3", "#D7FFE6", "#C535A9", "#260009", "#6A8781", "#A8ABB4", "#D45262",
    "#794B61", "#4621B2", "#8DA4DB", "#C7C890", "#6FE9AD", "#A243A7", "#B2B081", "#181B00",
    "#286154", "#4CA43B", "#6A9573", "#A8441D", "#5C727B", "#738671", "#D0CFCB", "#897B77",
    "#1F3F22", "#4145A7", "#DA9894", "#A1757A", "#63243C", "#ADAAFF", "#00CDE2", "#DDBC62",
    "#698EB1", "#208462", "#00B7E0", "#614A44", "#9BBB57", "#7A5C54", "#857A50", "#766B7E",
    "#014833", "#FF8347", "#7A8EBA", "#274740", "#946444", "#EBD8E6", "#646241", "#373917",
    "#6AD450", "#81817B", "#D499E3", "#979440", "#011A12", "#526554", "#B5885C", "#A499A5",
    "#03AD89", "#B3008B", "#E3C4B5", "#96531F", "#867175", "#74569E", "#617D9F", "#E70452",
    "#067EAF", "#A697B6", "#B787A8", "#9CFF93", "#311D19", "#3A9459", "#6E746E", "#B0C5AE",
    "#84EDF7", "#ED3488", "#754C78", "#384644", "#C7847B", "#00B6C5", "#7FA670", "#C1AF9E",
    "#2A7FFF", "#72A58C", "#FFC07F", "#9DEBDD", "#D97C8E", "#7E7C93", "#62E674", "#B5639E",
    "#FFA861", "#C2A580", "#8D9C83", "#B70546", "#372B2E", "#0098FF", "#985975", "#20204C",
    "#FF6C60", "#445083", "#8502AA", "#72361F", "#9676A3", "#484449", "#CED6C2", "#3B164A",
    "#CCA763", "#2C7F77", "#02227B", "#A37E6F", "#CDE6DC", "#CDFFFB", "#BE811A", "#F77183",
    "#EDE6E2", "#CDC6B4", "#FFE09E", "#3A7271", "#FF7B59", "#4E4E01", "#4AC684", "#8BC891",
    "#BC8A96", "#CF6353", "#DCDE5C", "#5EAADD", "#F6A0AD", "#E269AA", "#A3DAE4", "#436E83",
    "#002E17", "#ECFBFF", "#A1C2B6", "#50003F", "#71695B", "#67C4BB", "#536EFF", "#5D5A48",
    "#890039", "#969381", "#371521", "#5E4665", "#AA62C3", "#8D6F81", "#2C6135", "#410601",
    "#564620", "#E69034", "#6DA6BD", "#E58E56", "#E3A68B", "#48B176", "#D27D67", "#B5B268",
    "#7F8427", "#FF84E6", "#435740", "#EAE408", "#F4F5FF", "#325800", "#4B6BA5", "#ADCEFF",
    "#9B8ACC", "#885138", "#5875C1", "#7E7311", "#FEA5CA", "#9F8B5B", "#A55B54", "#89006A",
    "#AF756F", "#2A2000", "#7499A1", "#FFB550", "#00011E", "#D1511C", "#688151", "#BC908A",
    "#78C8EB", "#8502FF", "#483D30", "#C42221", "#5EA7FF", "#785715", "#0CEA91", "#FFFAED",
    "#B3AF9D", "#3E3D52", "#5A9BC2", "#9C2F90", "#8D5700", "#ADD79C", "#00768B", "#337D00",
    "#C59700", "#3156DC", "#944575", "#ECFFDC", "#D24CB2", "#97703C", "#4C257F", "#9E0366",
    "#88FFEC", "#B56481", "#396D2B", "#56735F", "#988376", "#9BB195", "#A9795C", "#E4C5D3",
    "#9F4F67", "#1E2B39", "#664327", "#AFCE78", "#322EDF", "#86B487", "#C23000", "#ABE86B",
    "#96656D", "#250E35", "#A60019", "#0080CF", "#CAEFFF", "#323F61", "#A449DC", "#6A9D3B",
    "#FF5AE4", "#636A01", "#D16CDA", "#736060", "#FFBAAD", "#D369B4", "#FFDED6", "#6C6D74",
    "#927D5E", "#845D70", "#5B62C1", "#2F4A36", "#E45F35", "#FF3B53", "#AC84DD", "#762988",
    "#70EC98", "#408543", "#2C3533", "#2E182D", "#323925", "#19181B", "#2F2E2C", "#023C32",
    "#9B9EE2", "#58AFAD", "#5C424D", "#7AC5A6", "#685D75", "#B9BCBD", "#834357", "#1A7B42",
    "#2E57AA", "#E55199", "#316E47", "#CD00C5", "#6A004D", "#7FBBEC", "#F35691", "#D7C54A",
    "#62ACB7", "#CBA1BC", "#A28A9A", "#6C3F3B", "#FFE47D", "#DCBAE3", "#5F816D", "#3A404A",
    "#7DBF32", "#E6ECDC", "#852C19", "#285366", "#B8CB9C", "#0E0D00", "#4B5D56", "#6B543F",
    "#E27172", "#0568EC", "#2EB500", "#D21656", "#EFAFFF", "#682021", "#2D2011", "#DA4CFF",
    "#70968E", "#FF7B7D", "#4A1930", "#E8C282", "#E7DBBC", "#A68486", "#1F263C", "#36574E",
    "#52CE79", "#ADAAA9", "#8A9F45", "#6542D2", "#00FB8C", "#5D697B", "#CCD27F", "#94A5A1",
    "#790229", "#E383E6", "#7EA4C1", "#4E4452", "#4B2C00", "#620B70", "#314C1E", "#874AA6",
    "#E30091", "#66460A", "#EB9A8B", "#EAC3A3", "#98EAB3", "#AB9180", "#B8552F", "#1A2B2F",
    "#94DDC5", "#9D8C76", "#9C8333", "#94A9C9", "#392935", "#8C675E", "#CCE93A", "#917100",
    "#01400B", "#449896", "#1CA370", "#E08DA7", "#8B4A4E", "#667776", "#4692AD", "#67BDA8",
    "#69255C", "#D3BFFF", "#4A5132", "#7E9285", "#77733C", "#E7A0CC", "#51A288", "#2C656A",
    "#4D5C5E", "#C9403A", "#DDD7F3", "#005844", "#B4A200", "#488F69", "#858182", "#D4E9B9",
    "#3D7397", "#CAE8CE", "#D60034", "#AA6746", "#9E5585", "#BA6200"]

emps_dict = {
    0: "Impyr",
    1: "Respov",
    2: "Fedyr",
    3: "Koved",
    4: "Lyg",
    5: "Kohl",
}

color_dict = {
    0: "aqua",
    1: "vela",
    2: "ughi",
    3: "marine",
    4: "oise",
    5: "garan",
    6: "kart",
    7: "bari",
    8: "chari",
    9: "ruse",
    10: "lagha",
    11: "uka",
    12: "use",
    13: "barh",
    14: "elbi",
    15: "chel",
    16: "ember",
}

colour_dict = {
    0: "burizh",
    1: "karam",
    2: "schuri",
    3: "oleanha",
    4: "dulme",
    5: "pahj",
    6: "khal",
    7: "yati",
    8: "dzhar",
    9: "akose",
    10: "yaul",
    11: "kery",
    12: "vagua",
    13: "byol",
    14: "bervaj",
    15: "hayen",
    16: "lyban",
}
SHRAD = HUBRAD * 0.1
SCRAD = CLUSRAD * 0.06
SDRAD = DISKRAD * 0.1
NUMCLUSA = NUMCLUS - DISCLUS
NUMCLUSB = NUMCLUS + DISCLUS
CLUSRADA = CLUSRAD - DISCLRAD
CLUSRADB = CLUSRAD + DISCLRAD
NUMCB = NUMC + 1
fempn = 0

def generateEmpires():
    starnum = random.randrange(0, int(starnumear))
    show_language(get_language())
    print wds
    starnames = []
    stern = 0
    empcl = str(random.choice(speccolor))
    empcolor = str(random.choice(color_dict)) + str(random.choice(color_dict)) + " " + str(random.choice(colour_dict)) + "(" + str(empcl) + ")"
    empst = random.choice(wds)
    while stern < starnum:
        strn = random.choice(wds)
        starnames.append(strn)
        stern = stern + 1
    empty = emps_dict[random.randrange(0,5)]
    empnp = str(empst) + " " + str(empty)
    EMPN = str(empnp) + str(RAND)
    with open("Spiral Galaxy" + str(RAND) + "-" + str(EMPN) + " " + ".txt", "w") as text_file:
        text_file.write("Empire Number: {}".format(RAND))
        text_file.write(" ")
        text_file.write("Empire Name: {}".format(empnp))
        text_file.write(" ")
        text_file.write("Empire Color: {}".format(empcolor))
        text_file.write(" ")
        text_file.write("Stars: {}".format(starnames))

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
        
        while fempn < empn:
            generateEmpires
    
        # Replaces the if/elif logic with a simple lookup. Faster and
        # and easier to read.
        scol = str(random.choice(speccolor))

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
        scol = str(random.choice(speccolor))

        # Add star to the stars array
        stars.append((x, y, z, scol))

        # Process next star
        i = i + 1
        sran = 0
        
    # Generate clusters and their stars.
    
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
                scol = str(random.choice(speccolor))
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