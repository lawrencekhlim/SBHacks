import urllib
master_url = "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/scores/gamedetail/0021700{}_gamedetail.json"
i = 0.0011
while i < 0.668:
    f = urllib.urlopen(master_url.format(str(i)[2:-1]))
    infile = open("game{}.json".format(str(i)[2:-1]),"w")
    infile.write(f.read())
    infile.close()
    print i, "game{}.json".format(str(i)[2:-1]),"w"
    i+=0.001