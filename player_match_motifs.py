'''

Matches player name to ID in common_motifs.csv, saves with name in common_motifs_names.csv

'''

import pandas as pd
import numpy as np
import csv

df_players = pd.read_csv('players.csv')
df_players = df_players[['wyId', 'shortName', 'firstName', 'lastName']]
df_players['firstName'] = df_players['firstName'].str.decode('unicode_escape')
df_players['lastName'] = df_players['lastName'].str.decode('unicode_escape')

df_players['firstName'] = df_players['firstName'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')  
df_players['lastName'] = df_players['lastName'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')  

players = {}

for index, row in df_players.iterrows():
	players[row['wyId']] = row['firstName'] + " " + row['lastName']

df_motifs = pd.read_csv('common_motifs.csv')

df_motifs.rename( columns={'Unnamed: 0':'player_id'}, inplace=True )
row_list = df_motifs['player_id'].tolist()

player_list = []

for i in range(0, len(row_list), 1):
	player_list.append(players.get(row_list[i]))


df_motifs.index = player_list
df_motifs = df_motifs.drop(columns = ['player_id'])
print(df_motifs.head(5))
df_motifs.dropna()
df_motifs.to_csv('common_motifs_names.csv')