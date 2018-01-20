import urllib
master_url = "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/20{}/scores/gamedetail/002{}00{}_gamedetail.json"
for yr in range(15,18):
    i = 0.0011
    while i < 0.668:
        f = urllib.urlopen(master_url.format(yr,yr,str(i)[2:-1]))
        infile = open("Yr{}game{}.json".format(yr,str(i)[2:-1]),"w")
        infile.write(f.read())
        infile.close()
        print i, "Yr{}game{}.json".format(yr,str(i)[2:-1]),"w"
        i+=0.001