import pandas as pd


all_games = pd.read_csv("WorldCupMatches.csv")
all_games_2018 = pd.read_csv("world_cup_2018_stats.csv")

print(all_games.columns)
print(all_games.head())
print(all_games_2018.columns)
print(all_games_2018.tail())



# ['Year', 'Datetime', 'Stage', 'Stadium', 'City', 'Home Team Name',
#        'Home Team Goals', 'Away Team Goals', 'Away Team Name',
#        'Win conditions', 'Attendance', 'Half-time Home Goals',
#        'Half-time Away Goals', 'Referee', 'Assistant 1', 'Assistant 2',
#        'RoundID', 'MatchID', 'Home Team Initials', 'Away Team Initials']


# ['Game', 'Group', 'Team', 'Opponent', 'Home/Away', 'Score', 'WDL',
#        'Pens?', 'Goals For', 'Goals Against', 'Pen Shootout For',
#        'Pen Shootout Against', 'Attempts', 'On-Target', 'Off-Target',
#        'Blocked', 'Woodwork', 'Corners', 'Offsides', 'Ball possession %',
#        'Pass Accuracy %', 'Passes', 'Passes Completed', 'Distance Covered km',
#        'Balls recovered', 'Tackles', 'Blocks', 'Clearances', 'Yellow cards',
#        'Red Cards', 'Second Yellow Card leading to Red Card',
#        'Fouls Committed']