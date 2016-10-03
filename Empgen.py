import random

RAND = random.randrange(0,99999999)

NUMHUB = 1000
NUMDISK = 1000
starnumpre = (NUMHUB + NUMDISK) / 10
starnumear = starnumpre * 3
starnum = random.randrange(0, int(starnumear))

mistarnum = starnum / 10
starnumb = starnum + 180

wds = []

class ListDict(object):
    def __init__(self):
        self.item_to_position = {}
        self.items = []

    def add_item(self, item):
        if item in self.item_to_position:
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items)-1

    def remove_item(self, item):
        position = self.item_to_position.pop(item)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.item_to_position[last_item] = position

    def choose_random_item(self):
        return random.choice(self.items)

import re
from collections import defaultdict


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
    
show_language(get_language())
print wds


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

speccolor = ["#FFFF00","#1CE6FF","#FF34FF","#FF4A46","#008941","#006FA6","#A30059","#FFDBE5","#7A4900","#0000A6","#63FFAC","#B79762","#004D43","#8FB0FF","#997D87","#5A0007","#809693","#FEFFE6","#1B4400","#4FC601","#3B5DFF","#4A3B53","#FF2F80","#61615A","#BA0900","#6B7900","#00C2A0","#FFAA92","#FF90C9","#B903AA","#D16100","#DDEFFF","#000035","#7B4F4B","#A1C299","#300018","#0AA6D8","#013349","#00846F","#372101","#FFB500","#C2FFED","#A079BF","#CC0744","#C0B9B2","#C2FF99","#001E09","#00489C","#6F0062","#0CBD66","#EEC3FF","#456D75","#B77B68","#7A87A1","#788D66","#885578","#FAD09F","#FF8A9A","#D157A0","#BEC459","#456648","#0086ED","#886F4C","#34362D","#B4A8BD","#00A6AA","#452C2C","#636375","#A3C8C9","#FF913F","#938A81","#575329","#00FECF","#B05B6F","#8CD0FF","#3B9700","#04F757","#C8A1A1","#1E6E00","#7900D7","#A77500","#6367A9","#A05837","#6B002C","#772600","#D790FF","#9B9700","#549E79","#FFF69F","#201625","#72418F","#BC23FF","#99ADC0","#3A2465","#922329","#5B4534","#FDE8DC","#404E55","#0089A3","#CB7E98","#A4E804","#324E72","#6A3A4C","#83AB58","#001C1E","#D1F7CE","#004B28","#C8D0F6","#A3A489","#806C66","#222800","#BF5650","#E83000","#66796D","#DA007C","#FF1A59","#8ADBB4","#1E0200","#5B4E51","#C895C5","#320033","#FF6832","#66E1D3","#CFCDAC","#D0AC94","#7ED379","#012C58","#7A7BFF","#D68E01","#353339","#78AFA1","#FEB2C6","#75797C","#837393","#943A4D","#B5F4FF","#D2DCD5","#9556BD","#6A714A","#001325","#02525F","#0AA3F7","#E98176","#DBD5DD","#5EBCD1","#3D4F44","#7E6405","#02684E","#962B75","#8D8546","#9695C5","#E773CE","#D86A78","#3E89BE","#CA834E","#518A87","#5B113C","#55813B","#E704C4","#00005F","#A97399","#4B8160","#59738A","#FF5DA7","#F7C9BF","#643127","#513A01","#6B94AA","#51A058","#A45B02","#1D1702","#E20027","#E7AB63","#4C6001","#9C6966","#64547B","#97979E","#006A66","#391406","#F4D749","#0045D2","#006C31","#DDB6D0","#7C6571","#9FB2A4","#00D891","#15A08A","#BC65E9","#FFFFFE","#C6DC99","#203B3C","#671190","#6B3A64","#F5E1FF","#FFA0F2","#CCAA35","#374527","#8BB400","#797868","#C6005A","#3B000A","#C86240","#29607C","#402334","#7D5A44","#CCB87C","#B88183","#AA5199","#B5D6C3","#A38469","#9F94F0","#A74571","#B894A6","#71BB8C","#00B433","#789EC9","#6D80BA","#953F00","#5EFF03","#E4FFFC","#1BE177","#BCB1E5","#76912F","#003109","#0060CD","#D20096","#895563","#29201D","#5B3213","#A76F42","#89412E","#1A3A2A","#494B5A","#A88C85","#F4ABAA","#A3F3AB","#00C6C8","#EA8B66","#958A9F","#BDC9D2","#9FA064","#BE4700","#658188","#83A485","#453C23","#47675D","#3A3F00","#061203","#DFFB71","#868E7E","#98D058","#6C8F7D","#D7BFC2","#3C3E6E","#D83D66","#2F5D9B","#6C5E46","#D25B88","#5B656C","#00B57F","#545C46","#866097","#365D25","#252F99","#00CCFF","#674E60","#FC009C","#92896B"]

vessel_dict = {
    0: "-class ",
    1: "-subclass ",
    2: "-type ",
    3: "-subtype ",
}

smallship_dict = {
    0: "Auxship",
    1: "Fighter",
    2: "Corvette",
    3: "Frigate",
    4: "Minicarrier",
    5: "Destroyer",
    6: "Cruiser",
    7: "Carrier",
    8: "Battleship",
    9: "Leviathan",
    10: "Civship",
}

auxship_dict = {
    0: "Nytvohl",
    1: "Rivvohl",
    2: "Sbayvohl",
}

fighter_dict = {
    0: "Yndirzavdo",
    1: "Fydar",
    2: "Vonvar",
    3: "Konvohl",
}

corvette_dict = {
    0: "mi-Kolpad",
    1: "ig-Kolpad",
    2: "Kolpad",
    3: "Vatrolvohl",
    4: "Nyzalvohl",
    5: "ja-Kolpad",
}

frigate_dict = {
    0: "Travrogud",
    1: "mi-Vrogud",
    2: "ig-Vrogud",
    3: "Vrogud",
    4: "ja-Vrogud",
    5: "mi-Jezdar",
    6: "ig-Jezdar",
}

minicarrier_dict = {
    0: "Vrogud-kerya",
    1: "Jezdar-kerya",
}

destroyer_dict = {
    0: "Jezdar",
    1: "ja-Jezdar",
}

cruiser_dict = {
    0: "Lyzh Jezdar",
    1: "tsu-Gryzihyr",
    2: "mi-Gryzihyr",
    3: "ig-Gryzihyr",
    4: "Gryzihyr",
    5: "ja-Gryzihyr",
}

carrier_dict = {
    0: "mi-Kerya",
    1: "ig-Kerya",
    2: "Kerya",
    3: "ja-Kerya",
}

battleship_dict = {
    0: "Zrakvohl",
    1: "Vaghulgryzihyr",
    2: "mi-Vaghulvohl",
    3: "Vaghulvohl",
    4: "ja-Vaghulvohl", 
}

leviathan_dict = {
    0: "Tyedmokht",
    1: "Hagermokht",
    2: "Ilavutan",
}

civship_dict = {
    0: "Pertar",
    1: "Lytenor",
    2: "Tigronar",
    3: "Sybuer"
}

civ = 20
aux = 10
fight = 55
corv = 30
frig = 15
micar = 4
dest = 4
cruis = 2
carr = 1
battl = 0.25
levi = 0.05

civn = civ * starnum
civra = random.randrange(1,civn)
civrb = str(civra) + "x "
civcla = random.choice(wds)
civclb = random.choice(vessel_dict)
civclc = random.choice(civship_dict)
civclass = str(civrb) + str(civcla) + str(civclb) + str(civclc)
auxn = aux * starnum
auxra = random.randrange(1,auxn)
auxrb = str(auxra) + "x "
auxcla = random.choice(wds)
auxclb = random.choice(vessel_dict)
auxclc = random.choice(auxship_dict)
auxclass = str(auxrb) + str(auxcla) + str(auxclb) + str(auxclc)
fightn = fight * starnum
fightra = random.randrange(1,fightn)
fightrb = str(fightra) + "x "
fightcla = random.choice(wds)
fightclb = random.choice(vessel_dict)
fightclc = random.choice(fighter_dict)
fightclass = str(fightrb) + str(fightcla) + str(fightclb) + str(fightclc)
corvn = corv * starnum
corvra = random.randrange(1,corvn)
corvrb = str(corvra) + "x "
corvcla = random.choice(wds)
corvclb = random.choice(vessel_dict)
corvclc = random.choice(corvette_dict)
corvclass = str(corvrb) + str(corvcla) + str(corvclb) + str(corvclc)
frign = frig * starnum
frigra = random.randrange(1,frign)
frigrb = str(frigra) + "x "
frigcla = random.choice(wds)
frigclb = random.choice(vessel_dict)
frigclc = random.choice(frigate_dict)
frigclass = str(frigrb) + str(frigcla) + str(frigclb) + str(frigclc)
micarn = micar * starnum
micarra = random.randrange(1,micarn)
micarrb = str(micarra) + "x "
micarcla = random.choice(wds)
micarclb = random.choice(vessel_dict)
micarclc = random.choice(minicarrier_dict)
micarclass = str(micarrb) + str(micarcla) + str(micarclb) + str(micarclc)
destn = dest * starnum
destra = random.randrange(1,destn)
destrb = str(destra) + "x "
destcla = random.choice(wds)
destclb = random.choice(vessel_dict)
destclc = random.choice(destroyer_dict)
destclass = str(destrb) + str(destcla) + str(destclb) + str(destclc)
cruisn = cruis * starnum
cruisra = random.randrange(1, cruisn)
cruisrb = str(cruisra) + "x "
cruiscla = random.choice(wds)
cruisclb = random.choice(vessel_dict)
cruisclc = random.choice(cruiser_dict)
cruisclass = str(cruisrb) + str(cruiscla) + str(cruisclb) + str(cruisclc)
carrn = carr * starnum
carrra = random.randrange(1, carrn)
carrrb = str(carrra) + "x "
carrcla = random.choice(wds)
carrclb = random.choice(vessel_dict)
carrclc = random.choice(carrier_dict)
carrclass = str(carrrb) + str(carrcla) + str(carrclb) + str(carrclc)
battln = battl * starnum
battlra = random.randrange(0, int(battln))
battlrb = str(battlra) + "x "
battlcla = random.choice(wds)
battlclb = random.choice(vessel_dict)
battlclc = random.choice(battleship_dict)
battlclass = str(battlrb) + str(battlcla) + str(battlclb) + str(battlclc)
levin = levi * starnum
levira = random.randrange(0, int(levin))
levirb = str(levira) + "x "
levicla = random.choice(wds)
leviclb = random.choice(vessel_dict)
leviclc = random.choice(leviathan_dict)
leviclass = str(levirb) + str(levicla) + str(leviclb) + str(leviclc)

starnuml = starnum - int(mistarnum)
starnumr = starnum + int(mistarnum)

civa = civ * random.randrange(starnuml,starnumr)
auxa = aux * random.randrange(starnuml,starnumr)
figha = fight * random.randrange(starnuml,starnumr)
corva = corv * random.randrange(starnuml,starnumr)
friga = frig * random.randrange(starnuml,starnumr)
micaa = micar * random.randrange(starnuml,starnumr)
desta = dest * random.randrange(starnuml,starnumr)
cruia = cruis * random.randrange(starnuml,starnumr)
carra = carr * random.randrange(starnuml,starnumr)
batta = battl * random.randrange(starnuml,starnumr)
levia = levi * random.randrange(starnuml,starnumr)

starnames = []
stern = 0

empcolor = str(random.choice(color_dict)) + str(random.choice(color_dict)) + " " + str(random.choice(colour_dict)) + "(" + str(random.choice(speccolor)) + ")"

empst = random.choice(wds)
while stern < starnum:
    strn = random.choice(wds)
    starnames.append(strn)
    stern = stern + 1
empty = emps_dict[random.randrange(0,5)]
empnp = str(empst) + " " + str(empty)
EMPN = str(empnp) + str(RAND)
with open(str(EMPN) + " " + ".txt", "w") as text_file:
    text_file.write("Empire Number: {}".format(RAND))
    text_file.write(" ")
    text_file.write("Empire Name: {}".format(empnp))
    text_file.write(" ")
    text_file.write("Empire Color: {}".format(empcolor))
    text_file.write(str(civclass))
    text_file.write(" ")
    text_file.write(str(auxclass))
    text_file.write(" ")
    text_file.write(str(fightclass))
    text_file.write(" ")                   
    text_file.write(str(corvclass))
    text_file.write(" ")
    text_file.write(str(frigclass))
    text_file.write(" ")               
    text_file.write(str(micarclass))
    text_file.write(" ")                
    text_file.write(str(destclass))
    text_file.write(" ")                
    text_file.write(str(cruisclass))
    text_file.write(" ")                
    text_file.write(str(carrclass))
    text_file.write(" ")                
    text_file.write(str(battlclass))
    text_file.write(" ")
    text_file.write(str(leviclass))
    text_file.write(" ")
    text_file.write(str(starnum))
    text_file.write(" ")
    text_file.write("Stars: {}".format(starnames))
    