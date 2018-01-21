#key: ref, val: dict with key team, val num techs
refereeTechs = {}

#key: ref, val: dict with key team, val num games
refereeGames = {}

for line in open("techfouls2015-7.csv", "r"):
    line = line.strip().split(",")
    refname, numtechs, numgames, techave, teamname = line
    teamname = line[4]
    
    if refname not in refereeTechs:
        refereeTechs[refname] = {}
    if teamname not in refereeTechs[refname]:
        refereeTechs[refname][teamname] = 0
    refereeTechs[refname][teamname] += int(numtechs)

    if refname not in refereeGames:
        refereeGames[refname] = {}
    if teamname not in refereeGames[refname]:
        refereeGames[refname][teamname] = 0
    refereeGames[refname][teamname] += int(numgames)


cutoff = 0.3
teamAboveCutoff = {}
teamBelowCutoff = {}

for ref in refereeTechs:
    for team, numtechs in refereeTechs[ref].items():
        if team not in teamAboveCutoff:
            teamAboveCutoff[team] = 0
            teamBelowCutoff[team] = 0
        if refereeTechs[ref][team]/refereeGames[ref][team] >= cutoff:
            teamAboveCutoff[team] += 1
        else:
            teamBelowCutoff[team] += 1

f = open("techfoulratios.csv", "w")
for team, numcutoff in teamAboveCutoff.items():
    f.write(team + "," + str(numcutoff) + "," + str(teamBelowCutoff[team] + teamAboveCutoff[team]) + "\n")

f.close()


