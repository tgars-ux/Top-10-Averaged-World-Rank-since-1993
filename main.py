import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
%matplotlib inline
import numpy as np
import seaborn as sns

# Historical FIFA rankings dataframe
historical_rankings = pd.read_csv('fifa_ranking.csv')
# Historical match between 2 teams dataframe
historical_matches = pd.read_csv('results.csv')
world_cup = pd.read_csv('World Cup 2018 Dataset.csv')

historical_rankings = historical_rankings.replace({'IR Iran': 'Iran'})
historical_matches = historical_matches.replace({'Germany DR': 'Germany', 'China': 'China PR'})
world_cup = world_cup.replace({"IRAN": "Iran", 
                               "Costarica": "Costa Rica", 
                               "Porugal": "Portugal", 
                               "Columbia": "Colombia", 
                               "Korea" : "Korea Republic"})
world_cup = world_cup.set_index('Team')

print("Historical FIFA Rankings:")
print(historical_rankings.info())
print("--------------------------------")
print("Historical matches")
print(historical_matches.info())

historical_rankings = historical_rankings.loc[:,['rank', 'country_full','country_abrv', 'total_points', 'confederation', 'rank_date']]
historical_rankings['rank_date'] = pd.to_datetime(historical_rankings['rank_date'])
historical_rankings = historical_rankings.set_index(['rank_date'])\
            .groupby(['country_full'], group_keys=False)\
            .resample('D').first()\
            .fillna(method='ffill')\
            .reset_index()
historical_rankings.head()

historical_rankings_by_team = historical_rankings.groupby([historical_rankings.rank_date.dt.year,historical_rankings.country_full]).mean()
historical_rankings_by_team = historical_rankings_by_team.reset_index()

print("Top 10 Averaged World Rank since 1993")
historical_rankings_by_team.groupby(['country_full']).mean().sort_values(by=['rank'])['rank'][:10]

print("Top 32 Teams Averaged World Rank That Failed to Qualify to World Cup 2018")
top_32 = historical_rankings_by_team.groupby(['country_full']).mean().sort_values(by=['rank'])['rank'][:32].reset_index()
not_in_world_cup_2018 = top_32[top_32['country_full'].isin(world_cup.index.unique())]
print(not_in_world_cup_2018)
