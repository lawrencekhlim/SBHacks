import json
import scipy
import numpy as np
from scipy import linalg
import matplotlib
import csv


teamnameID = {
    "Hawks": 0,
    "Celtics": 1,
    "Nets": 2,
    "Hornets": 3,
    "Bulls": 4,
    "Cavaliers": 5,
    "Mavericks": 6,
    "Nuggets": 7,
    "Pistons": 8,
    "Warriors": 29,
    "Rockets": 10,
    "Pacers": 11,
    "Clippers": 12,
    "Lakers": 13,
    "Grizzlies": 14,
    "Heat": 15,
    "Bucks": 16,
    "Timberwolves": 17,
    "Pelicans": 18,
    "Knicks": 19,
    "Thunder": 20,
    "Magic": 21,
    "76ers": 22,
    "Suns": 23,
    "Trail Blazers": 24,
    "Jazz": 25,
    "Kings": 26,
    "Spurs": 27,
    "Raptors": 28,
    "Wizards": 9
}

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


officialtohomefouls = {}
officialtoawayfouls = {}

homesum = 0
awaysum = 0


def updateOfficialsFouls(officials):
    for official in officials:
        if official in officialtohomefouls:
            officialtohomefouls[official].append (homefouls)
        else:
            officialtohomefouls[official] = [homefouls]

        if official in officialtoawayfouls:
            officialtoawayfouls[official].append (awayfouls)
        else:
            officialtoawayfouls[official] = [awayfouls]

def getHomeFoulAverage():
    return (float) (homesum)/666

def getAwayFoulAverage():
    return (float) (awaysum)/666

matrixA = []
matrixD = []
matrixTotal = []
vectorB = []
vectorC = []
vectorTotal = []

for i in range (1, 668):

    path = "data/Yr15game{:03d}.json".format(i)
    # path
    json_file = open(path, "r")
    json_text = json_file.read()
    json_file.close()
    try:
        json_dict = json.loads(json_text)
    except:
         ('FAILED GAME ' + str(i))


    officials = []
    for i in range (0, 3):
        try:
            officials.append(int(json_dict[u'g'][u'offs'][u'off'][i][u'num']))
        except:
             ('FAILED GAME ' + str(i))

    homefouls = int(json_dict[u'g'][u'hls'][u'tstsg'][u'pf'])
    homesum += homefouls

    awayfouls = int(json_dict[u'g'][u'vls'][u'tstsg'][u'pf'])
    awaysum += awayfouls

    teams = [0] * 30
    hometeam = str(json_dict[u'g'][u'hls'][u'tn'])
    awayteam = str(json_dict[u'g'][u'vls'][u'tn'])
    teams[teamnameID[hometeam]] = 1
    teams[teamnameID[awayteam]] = 1

    matrixD.append (teams)


    # for the matrix
    row = [0] * 78
    for off in officials:
        row[int (off)] = 1
    
    matrixTotal.append (row + teams)
    matrixA.append(row)
    vectorTotal.append ([homefouls + awayfouls])
    vectorB.append([homefouls])
    vectorC.append([awayfouls])

    #update the dicts with the referees' fouls for the game
    updateOfficialsFouls(officials)

# Find average of fouls for home and array
averagehome = getHomeFoulAverage()
averageaway = getAwayFoulAverage()

averagenumhomefouls = {}
averagenumawayfouls = {}
variancehomefouls = {}
varianceawayfouls = {}
averagebias = {}

# Calculate each ref's average fouls they call at home
for key, value in officialtohomefouls.items():
    averagenumhomefouls[key] = (float)(sum(value))/len(value)
    averagebias [key] = -1 * averagenumhomefouls[key]
    variancehomefouls [key] = 0
    for foul in officialtohomefouls[key]:
        variancehomefouls[key]+= (averagenumhomefouls[key] - foul)**2
    variancehomefouls[key] /= len (officialtohomefouls[key])

# Calculate each ref's average fouls they call away
for key, value in officialtoawayfouls.items():
    averagenumawayfouls[key] = (float)(sum(value))/len(value)
    averagebias [key] +=averagenumawayfouls[key]
    varianceawayfouls [key] = 0
    for foul in officialtoawayfouls[key]:
        varianceawayfouls[key]+= (averagenumawayfouls[key] - foul)**2
    varianceawayfouls[key] /= len (officialtoawayfouls[key])


print "AWAY TEAM"
print averagenumawayfouls
print max (averagenumawayfouls.values())
print "HOME TEAM"
print averagenumhomefouls
print max (averagenumhomefouls.values())



print averageaway
print averagehome


print "BIAS"
print sorted(averagebias, key= lambda x: averagebias[x])

print variancehomefouls

print matrixA
vectorX = linalg.lstsq(matrixA,vectorB)

print vectorX

vectorY = linalg.lstsq(matrixA, vectorC)
f = open ("normalizedHomeFouls.csv", "w")
csvwriter = csv.writer (f)
csvwriter.writerow(["Official Names", "Linearized Home Fouls Given", "Linearized Away Fouls Given", "Home Fouls - Away Fouls"])
for i in range (len (vectorX[0])):
    if i in officialsNames and vectorX[0][i][0] > 0.5:
        csvwriter.writerow ([officialsNames[i],vectorX[0][i][0], vectorY[0][i][0], vectorX[0][i][0]-vectorY[0][i][0]])
f.close()


arr = [i for i in range(78)] +[key for key in sorted(teamnameID, key= lambda x: teamnameID[x])]
for i in range (len (vectorX[0])):
     (str(arr[i]) + ": " + str(vectorX [0][i][0]) )

f = open ("Referees.csv", "w")
csvwriter = csv.writer (f)


csvwriter.writerow(arr + ["Home Team Fouls", "Away Team Fouls", "Total Team Fouls"])
for i in range (len (matrixTotal)):
    csvwriter.writerow (matrixTotal[i] + [vectorB[i][0], vectorC[i][0], vectorTotal[i][0]])
f.close()
#f.write ("," + str ()

