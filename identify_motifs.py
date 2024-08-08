'''

Reads event data from top 5 leagues, identifies passing motif per player, saves most common motifs into common_motifs.csv

'''

import pandas as pd
import numpy as np
import csv

#england
df_eng = pd.read_csv('soccer_event_data/england.csv', index_col=0)
df_eng = df_eng[['sub_event_name', 'player_id', 'match_id', 'event_name', 'team_id', 'poss_id', 'event_sec']]
df_eng['lag'] = df_eng['event_sec'].shift(1)
df_eng['lag'] = df_eng['lag'].fillna(0)
df_eng['duration'] = df_eng['event_sec'] - df_eng['lag']
df_eng = df_eng.drop(columns=['lag', 'event_sec'])
df_eng.to_csv("england_mod.csv")

#france
df_fra = pd.read_csv('soccer_event_data/france.csv', index_col=0)
df_fra = df_fra[['sub_event_name', 'player_id', 'match_id', 'event_name', 'team_id', 'poss_id', 'event_sec']]
df_fra['lag'] = df_fra['event_sec'].shift(1)
df_fra['lag'] = df_fra['lag'].fillna(0)
df_fra['duration'] = df_fra['event_sec'] - df_fra['lag']
df_fra = df_fra.drop(columns=['lag', 'event_sec'])
df_fra.to_csv("france_mod.csv")

#germany
df_ger = pd.read_csv('soccer_event_data/germany.csv', index_col=0)
df_ger = df_ger[['sub_event_name', 'player_id', 'match_id', 'event_name', 'team_id', 'poss_id', 'event_sec']]
df_ger['lag'] = df_ger['event_sec'].shift(1)
df_ger['lag'] = df_ger['lag'].fillna(0)
df_ger['duration'] = df_ger['event_sec'] - df_ger['lag']
df_ger = df_ger.drop(columns=['lag', 'event_sec'])
df_ger.to_csv("germany_mod.csv")

#italy
df_ita = pd.read_csv('soccer_event_data/italy.csv', index_col=0)
df_ita = df_ita[['sub_event_name', 'player_id', 'match_id', 'event_name', 'team_id', 'poss_id', 'event_sec']]
df_ita['lag'] = df_ita['event_sec'].shift(1)
df_ita['lag'] = df_ita['lag'].fillna(0)
df_ita['duration'] = df_ita['event_sec'] - df_ita['lag']
df_ita = df_ita.drop(columns=['lag', 'event_sec'])
df_ita.to_csv("italy_mod.csv")

#spain
df_esp = pd.read_csv('soccer_event_data/spain.csv', index_col=0)
df_esp = df_esp[['sub_event_name', 'player_id', 'match_id', 'event_name', 'team_id', 'poss_id', 'event_sec']]
df_esp['lag'] = df_esp['event_sec'].shift(1)
df_esp['lag'] = df_esp['lag'].fillna(0)
df_esp['duration'] = df_esp['event_sec'] - df_esp['lag']
df_esp = df_esp.drop(columns=['lag', 'event_sec'])
df_esp.to_csv("spain_mod.csv")

df_list = [df_eng, df_fra, df_ger, df_ita, df_esp]
first_match = [2499719, 2500686, 2516739, 2575959, 2565548]
num_matches = [379, 379, 305, 379, 379]

player_motifs = {}

for country_num in range(0,5,1):
	for j in range(0,num_matches[country_num],1):
		df_match = df_list[country_num]
		df_match = df_match[df_match['match_id'] == first_match[country_num]+j]
		max_pos = df_match['poss_id'].max()
		print(max_pos)
		for i in range(1,max_pos,1):
			#match = 2499719+j
			df_poss = df_match[(df_match['poss_id'] == i) & (df_match['event_name'].isin(['Pass', 'Free Kick', 'Shot']))]	

			df_poss.index = np.arange(0, len(df_poss.duration)) # you could also do df.reset_index()
			df_poss = df_poss[df_poss.duration <= 5]
			list_of_df = np.split(df_poss, np.flatnonzero(np.diff(df_poss.index) != 1) + 1)
			#print(len(list_of_df))

			for df_poss in list_of_df:

				if (len(df_poss['team_id'].unique()) and len(df_poss) <= 5):	

					#print(df_poss)

					for i in range(0,len(df_poss),1):
						

						pip_all = []
						pip_unique = []
						for player in df_poss['player_id']:
							pip_all.append(player)
							if(player not in pip_unique):
								pip_unique.append(player)

						pip_all_copy = pip_all
						player_dict = {}
						current_player = pip_all[i]
						motif = ""
						counter = 2
						one_count = 0
						shot = []
						indexes = list(df_poss.index.values)

						for j in range(0,len(pip_all),1):
							if pip_all_copy[j] == current_player:
								pip_all_copy[j] = 1
								one_count = one_count + 1
							elif pip_all[j] not in player_dict:
								player_dict[pip_all[j]] = counter
								counter = counter + 1
						
						for k in range (0,len(pip_all_copy),1):	
							if pip_all_copy[k] == 1:
								motif = motif + "1"
								if(df_poss.at[indexes[k],'event_name'] == 'Shot'):
									shot.append(True)
								else:
									shot.append(False)
							else:
								motif = motif + str(player_dict.get(pip_all_copy[k]))
								if(df_poss.at[indexes[k],'event_name'] == 'Shot'):
									shot.append(True)
								else:
									shot.append(False)

						if shot[len(shot)-1] == True:
							motif = motif[:-1]
							motif = motif + "S"

						if(len(motif) >= 3):
							if(current_player not in player_motifs):
								mlist = []
								player_motifs[current_player] = mlist
								player_motifs.get(current_player).append(motif)
							else:
								player_motifs.get(current_player).append(motif)



					if(len(motif) >= 3 and len(motif) <= 5):
						removed = 0
						if one_count > 1:
							while(removed < one_count-1):
								for m in player_motifs.get(current_player):
									if m == motif:
										player_motifs.get(current_player).remove(m)
										removed = removed + 1

	print("done")


unique_motifs = []
unique_players = []

for player in player_motifs:
	for m in player_motifs.get(player):
		if m not in unique_motifs:
			unique_motifs.append(m)
	unique_players.append(player)

sorted_motifs = sorted(unique_motifs)

players_array = np.zeros((len(player_motifs), len(sorted_motifs)))

df = pd.DataFrame(players_array)
df.columns = sorted_motifs
df.index = unique_players

for player in unique_players:
	for motif in sorted_motifs:
		count = 0
		for m in player_motifs.get(player):
			if m == motif:
				count = count + 1
		df.at[player, motif] = int(count)

df_common = df[['121', '123', '231', '213', '212', '1234', '1213', '1232', '2134', '2132', '1212', '2313', '2312', 
				'121S', '123S', '231S', '213S', '212S', '1234S', '1213S', '1232S', '2134S', '2132S', '1212S', '2313S', '2312S',
				'12S', '21S', '23S',]]
df_common.to_csv("common_motifs.csv")





