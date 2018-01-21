import json
import scipy
import numpy as np
from scipy import linalg
import csv
import copy

officialsNames = {
    3:"Nick Buchert",
    4:"Sean Wright",
    5:"Kane Fitzgerald",
    6:"Tony Brown",
    7:"Lauren Holtkamp",
    8:"Marc Davis",
    9: "Derrick Stafford",
    10: "Ron Garretson",
    11:"Derrick Collins",
    12:"CJ Washington",
    13:"Monty McCutchen",
    14:"Ed Malloy",
    15:"Zach Zarba",
    16:"David Guthrie",
    17:"Jonathan Sterling",
    18:"Matt Boland",
    19:"James Capers",
    20:"Leroy Richardson",
    21:"Dedric Taylor",
    22:"Bill Spooner",
    23:"Jason Phillips",
    24:"Mike Callahan",
    25:"Tony Brothers",
    26:"Pat Fraher",
    27:"Mitchell Ervin",
    28:"Kevin Scott",
    29:"Mark Lindsay",
    30:"John Goble",
    31:"Scott Wall",
    32:"Marat Kogut",
    33:"Sean Corbin",
    34:"Kevin Cutler",
    35:"Jason Goldenberg",
    36:"Brent Barnaky",
    37:"Eric Dalen",
    38:"Michael Smith",
    39:"Tyler Ford",
    40:"Leon Wood",
    41:"Ken Mauer",
    42:"Eric Lewis",
    44:"Brett Nansel",
    45:"Brian Forte",
    46:"Ben Taylor",
    47:"Bennie Adams",
    48:"Scott Foster",
    49:"Tom Washington",
    50:"Gediminas Petraitis",
    51:"Aaron Smith",
    52:"Scott Twardoski",
    54:"Ray Acosta",
    55:"Bill Kennedy",
    56:"Mark Ayotte",
    58:"Josh Tiven",
    59:"Gary Zielinski",
    60:"James Williams",
    61:"Courtney Kirkland",
    62:"JB DeRosa",
    63:"Derek Richardson",
    64:"Justin Van Duyne",
    66:"Haywoode Workman",
    68:"Jacyn Goble",
    71:"Rodney Mott",
    72:"J.T. Orr",
    73:"Tre Maddox",
    74:"Curtis Blair",
    77:"Karl Lane",
    43:"Matt Myers",
    53:"Randy Richardson",
    67:"Brandon Adair",
    70:"Phenizee Ransom",
    76:"Vladimir Voyard-Tadal",
}

teams = {
"Hawks": 0,
"Celtics": 0,
"Nets": 0,
"Hornets": 0,
"Bulls": 0,
"Cavaliers": 0,
"Mavericks": 0,
"Nuggets": 0,
"Pistons": 0,
"Warriors": 0,
"Rockets": 0,
"Pacers": 0,
"Clippers": 0,
"Lakers": 0,
"Grizzlies": 0,
"Heat": 0,
"Bucks": 0,
"Timberwolves": 0,
"Pelicans": 0,
"Knicks": 0,
"Thunder": 0,
"Magic": 0,
"76ers": 0,
"Suns": 0,
"Trail Blazers": 0,
"Kings": 0,
"Spurs": 0,
"Raptors": 0,
"Jazz": 0,
"Wizards": 0
}
#key = officalnum, value = dict with key being team name and val being number of techs
officialtechs = {}

for i in range (1, 668):
    path = "data/Yr17game{:03d}.json".format(i)
    print(path)
    json_file = open(path, "r")
    json_text = json_file.read()
    json_file.close()
    try:
        json_dict = json.loads(json_text)
    except:
        print ('FAILED GAME ' + str(i))
    
    
    officials = []
    for i in range (0, 3):
        try:
            officials.append(int(json_dict[u'g'][u'offs'][u'off'][i][u'num']))
        except:
            pass
    hometechfouls = int(json_dict[u'g'][u'hls'][u'tstsg'][u'tf'])
    hometeamname = str(json_dict[u'g'][u'hls'][u'tn'])
    awaytechfouls = int(json_dict[u'g'][u'vls'][u'tstsg'][u'tf'])
    awayteamname = json_dict[u'g'][u'vls'][u'tn']

    for official in officials:
        if official not in officialtechs:
            officialtechs[official] = copy.deepcopy(teams)
        officialtechs[official][hometeamname] += hometechfouls
        officialtechs[official][awayteamname] += awaytechfouls

f = open("techfouls2017.csv", "w")
for officialnum in sorted(officialtechs.keys(), key = lambda x: x):
    line = ""
    line += str(officialnum) + ","
    for team in sorted(officialtechs[officialnum], key = lambda x: x):
        line += str(officialtechs[officialnum][team]) + ","

    f.write(line[:-1] + "\n")
f.close()

