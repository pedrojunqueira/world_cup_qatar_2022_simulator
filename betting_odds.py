import pandas as pd


df = pd.read_csv("betting_odds.csv", sep=";")

# print(df.columns)

# print(df.head())

flip = df.melt(id_vars=['group', 'team', 'code'])

avg_odds_by_team = flip.groupby(["team","code"])[["value"]].mean()

avg_odds_by_team = avg_odds_by_team.reset_index()

avg_odds_by_team = avg_odds_by_team.sort_values(by="value")

# avg_odds_by_team.to_csv("avg_odds_team.csv",index=False)

def get_odds(team:str,odds:pd.DataFrame)->float:
    return odds[odds["team"]==team]["value"].values[0]

print(get_odds("Brazil",avg_odds_by_team))