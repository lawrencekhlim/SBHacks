import json
from pprint import pprint

officialtohomefouls = {}
officialtoawayfouls = {}

homesum = 0
awaysum = 0
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
    #print officials

    homefouls = int(json_dict[u'g'][u'hls'][u'tstsg'][u'pf'])
    homesum += homefouls
    #print homefouls
    
    awayfouls = int(json_dict[u'g'][u'vls'][u'tstsg'][u'pf'])
    awaysum += awayfouls
    #   print awayfouls

    for official in officials:
        if official in officialtohomefouls:
            officialtohomefouls[official].append (homefouls)
        else:
            officialtohomefouls[official] = [homefouls]

        if official in officialtoawayfouls:
            officialtoawayfouls[official].append (awayfouls)
        else:
            officialtoawayfouls[official] = [awayfouls]

averagehome = (float) (homesum)/666
averageaway = (float) (awaysum)/666

averagenumhomefouls = {}
averagenumawayfouls = {}
averagebias = {}
for key, value in officialtohomefouls.items():
    averagenumhomefouls[key] = (float)(sum(value))/len(value)
    averagebias [key] = -1 * averagenumhomefouls[key]
for key, value in officialtoawayfouls.items():
    averagenumawayfouls[key] = (float)(sum(value))/len(value)
    averagebias [key] +=averagenumawayfouls[key]
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

f = open ("bias.csv", "w")
for key, value in averagebias.items():
    f.write (str(key) + ","+str(value)+"\n")

