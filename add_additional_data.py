'''

adds additional bio data and season stats to dataset for each player

'''

import pandas as pd
import numpy as np
import csv

df_eng = pd.read_csv('playerdata/premdata.csv')
df_fra = pd.read_csv('playerdata/francedata.csv')
df_ger = pd.read_csv('playerdata/germanydata.csv')
df_ita = pd.read_csv('playerdata/italydata.csv')
df_esp = pd.read_csv('playerdata/spaindata.csv')

df_list = [df_eng, df_fra, df_ger, df_ita, df_esp]

df_full = pd.read_csv('common_motifs_names4.csv')

players = {}
for df in df_list:
	for index, row in df.iterrows():
		statlist = []
		statlist.append(int(row['Age']))
		statlist.append(int(row['MP']))
		statlist.append(int(row['Goals']))
		statlist.append(int(row['Assists']))
		statlist.append(float(row['xGp90']))
		statlist.append(float(row['xAp90']))
		statlist.append(int(row['ChCr']))
		statlist.append(int(row['YC']))
		statlist.append(int(row['RC']))
		statlist.append(int(row['Tackles']))
		statlist.append(int(row['Pressures']))
		statlist.append(row['Player'].split())
		players[row['Player']] = statlist

	for player in players:
		for index, row in df_full.iterrows():
			if all(x in row['Player'] for x in players.get(player)[11]):
				name = " ".join(players.get(player)[11])
				df_full.at[index,'Age'] = int(players.get(name)[0])
				df_full.at[index,'MP'] = players.get(name)[1] 
				df_full.at[index,'Goals'] = players.get(name)[2]
				df_full.at[index,'Assists'] = players.get(name)[3]
				df_full.at[index,'xGp90'] = players.get(name)[4]
				df_full.at[index,'xAp90'] = players.get(name)[5]
				df_full.at[index,'ChCr'] = players.get(name)[6]
				df_full.at[index,'YC'] = players.get(name)[7]
				df_full.at[index,'RC'] = players.get(name)[8]
				df_full.at[index,'Tackles'] = players.get(name)[9]
				df_full.at[index,'Pressures'] = players.get(name)[10]

df_more = pd.read_csv('player_values.csv')

players2 = {}
for index, row in df_more.iterrows():
	value = []
	value.append(int(row['market_value']))
	value.append(row['position'])
	value.append(row['player_id'].split())
	players2[row['player_id']] = value

for player in players2:
	for index, row in df_full.iterrows():
		if all(x in row['Player'] for x in players2.get(player)[2]):
			name = " ".join(players2.get(player)[2])
			df_full.at[index,'Position'] = players2.get(name)[1]
			df_full.at[index,'Value'] = players2.get(name)[0]

df_cut = df_full.dropna()
df_cut.to_csv('fulldata.csv')