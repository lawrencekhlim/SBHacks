import json
import scipy
import numpy as np
from scipy import linalg
import csv

officialtohomefouls = {}
officialtoawayfouls = {}

homesum = 0
awaysum = 0

matrixA = []
vectorB = []
vectorC = []

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


for i in range (1, 668):

    path = "data/game{:03d}.json".format(i)
    print path
    json_file = open(path, "r")
    json_text = json_file.read()
    json_file.close()
    try:
        json_dict = json.loads(json_text)
    except:
        print ('FAILED GAME ' + str(i))


    officials = []
    for i in range (0, 3):
        officials.append(int(json_dict[u'g'][u'offs'][u'off'][i][u'num']))

    homefouls = int(json_dict[u'g'][u'hls'][u'tstsg'][u'pf'])
    homesum += homefouls

    awayfouls = int(json_dict[u'g'][u'vls'][u'tstsg'][u'pf'])
    awaysum += awayfouls

    # for the matrix
    row = [0] * 78
    for i in range (0, 3):
        row[officials[i]] = 1
    matrixA.append(row)
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


vectorX = linalg.lstsq(matrixA,vectorB)

print vectorX
f = open ("Referees.csv", "w")
csvwriter = csv.writer (f)
csvwriter.writerow([i for i in range(78)] + ["Home Team Fouls", "Away Team Fouls"])
for i in range (len (matrixA)):
    csvwriter.writerow (matrixA[i]+ [vectorB[i][0], vectorC[i][0]])
#f.write ("," + str ()

