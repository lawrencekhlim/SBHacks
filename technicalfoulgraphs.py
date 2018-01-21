from make_graph import MakeGraph
figurexvals = []
figureyvals = []

refteamtechs = {}
for line in open("techfouls2015.csv", "r"):
    line = line.split(",")
    refnum, numtechs, team = int(line[0]), int(line[1]), line[2]
    if refnum not in refteamtechs:
        refteamtechs[refnum] = {}
        refteamtechs[refnum][team] = numtechs
    else:
        if team not in refteamtechs[refnum]:
            refteamtechs[refnum][team] = numtechs
        else:
            print("ERROR")

    figurexvals.append(refnum)
    figureyvals.append(numtechs)

color = ["brown","brown","black", "cyan","cyan", "cyan", "magenta", "black", "magenta", "magenta", "black", "orange","orange", "orange","red", "red","red","black","yellow", "yellow", "black", "yellow", "green", "green", "green","black", "blue","blue"]*100
graph = MakeGraph()
graph.draw_figure_no_sort(figurexvals, figureyvals, "Referee Number", "Number of Technical Fouls", "Referees are power hungry dudes", color)
graph.show_plts()

