import json
import scipy
import numpy as np
from scipy import linalg
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
    "Warriors": 9,
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
    "Wizards": 29
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

    path = "data/Yr17game{:03d}.json".format(i)
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
        try:
            officials.append(int(json_dict[u'g'][u'offs'][u'off'][i][u'num']))
        except:
            print ('FAILED GAME ' + str(i))

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
        row[off] = 1
    
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


vectorX = linalg.lstsq(matrixTotal,vectorTotal)


arr = [i for i in range(78)] +[key for key in sorted(teamnameID, key= lambda x: teamnameID[x])]
for i in range (len (vectorX[3])):
    print (str(arr[i]) + ": " + str(vectorX [3][i]) )


f = open ("Referees.csv", "w")
csvwriter = csv.writer (f)

csvwriter.writerow(arr + ["Home Team Fouls", "Away Team Fouls", "Total Team Fouls"])
for i in range (len (matrixTotal)):
    csvwriter.writerow (matrixTotal[i] + [vectorB[i][0], vectorC[i][0], vectorTotal[i][0]])
#f.write ("," + str ()

