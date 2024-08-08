'''

Creates condensed dataset containing player name and market value

'''

import pandas as pd
players = {}
positions = {}

df_players = pd.read_csv('values/player_names.csv')
for index, row in df_players.iterrows():
	players[row['player_id']] = row['pretty_name']
	positions[row['pretty_name']] = row['sub_position']

df_values = pd.read_csv('values/player_valuations.csv')
df_values.replace({'player_id':players}, inplace=True)

for index, row in df_values.iterrows():
	df_values.at[index,'position'] = positions.get(row['player_id'])


df_values.to_csv('player_values.csv')
