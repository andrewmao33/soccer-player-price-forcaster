'''

Only save player valuations during summer transfer window months (May-July)

'''


import pandas as pd

df = pd.read_csv('values/all_player_values.csv')

#df = df.loc[df['date'].str.contains('2018-05') df['date'].str.contains('2018-06')]
valid = ('2018-05', '2018-06', '2018-07')
df = df[df['date'].str.startswith(valid)]
df.to_csv('values/player_valuations.csv')

