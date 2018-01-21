import json
import scipy
import numpy as np
from scipy import linalg
import csv
import copy

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

