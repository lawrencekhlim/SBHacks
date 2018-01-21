import json
import scipy
import numpy as np
from scipy import linalg
import csv
import copy

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
            officialtechs[official] = {}
            officialtechs[official][hometeamname] = hometechfouls
        else:
            if hometeamname not in officialtechs[official]:
                officialtechs[official][hometeamname] = hometechfouls
            else:
                officialtechs[official][hometeamname] += hometechfouls

        if official not in officialtechs:
            officialtechs[official] = {}
            officialtechs[official][awayteamname] = awaytechfouls
        else:
            if awayteamname not in officialtechs[official]:
                officialtechs[official][awayteamname] = awaytechfouls
            else:
                officialtechs[official][awayteamname] += awaytechfouls

f = open("techfouls2017.csv", "w")
for officialnum in sorted(officialtechs.keys(), key = lambda x: x):
    for team in sorted(officialtechs[officialnum], key = lambda x: x):
        f.write(str(officialnum) + "," + str(officialtechs[officialnum][team]) + "," + str(team) + "\n")
f.close()

