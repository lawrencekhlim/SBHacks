import json
import csv
from pprint import pprint

#player stats
def get_player_stats(player_dict):
	player_stats = []
	for player in player_dict:
		player_name = player[u'fn'] + u' ' +  player[u'ln']
		assists = player[u'ast']
		blocks = player[u'blk']
		dreb = player[u'dreb']
		fta = player[u'fta']
		ftm = player[u'ftm']
		oreb = player[u'oreb']
		pf = player[u'pf']
		points = player[u'pts']
		rebounds = player[u'reb']
		steals = player[u'stl']
		seconds_played = player[u'totsec']
		
		player_stats.append([player_name, assists, blocks, dreb, fta, ftm, oreb, pf, points, rebounds, steals, seconds_played])
	return player_stats
		



def writeJSON(file_path):
	print(file_path)
	
	data = json.load(open(file_path))



	data = data[u'g']

	at_city = data[u'ac']
	id = data[u'gid']
			
			
	home_stats = data[u'hls']
	home_name = home_stats[u'tc'] + home_stats[u'tn'] # team city + team name
	home_points = int(home_stats[u's'])
	home_player_stats = get_player_stats(home_stats[u'pstsg'])
	

	visiting_stats = data[u'vls']
	visiting_name = visiting_stats[u'tc'] + visiting_stats[u'tn'] # team city + team name
	visiting_points = int(visiting_stats[u's'])
	visiting_player_stats = get_player_stats(visiting_stats[u'pstsg'])

	for player in home_player_stats:
		#player stats, game id, team name, isHome, Against, Won
		player.extend([id, home_name, True, visiting_name, home_points > visiting_points])
		csvwriter.writerow(player)
		
	for player in visiting_player_stats:
		#player stats, game id, team name, isHome, Against, Won
		player.extend([id, visiting_name, False, home_name, visiting_points > home_points])
		csvwriter.writerow(player)
		

player_file = open("data/players.csv", "w")#, 'a')
csvwriter = csv.writer(player_file)

header = ["Player_Name", "Assists", "Blocks", "DREB", "FTA", "FTM", "OREB", "PF", "Points", "Rebounds", "Steals", "Seconds_Played", "Game_ID", "Team_Name", "isHome", "Playing_Against", "Won"]
csvwriter.writerow(header)

i = 0.0011
while i < 0.668:
	try:
		writeJSON('data/game{}.json'.format(str(i)[2:-1]))
	except:
		print("Not JSON")
	i+=.001

