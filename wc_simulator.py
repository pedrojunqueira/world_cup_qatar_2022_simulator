from random import randint, choice, random
from itertools import combinations
from collections import defaultdict, Counter

import pandas as pd

Groups = {"A":["Qatar","Ecuador","Senegal","Netherlands"],
          "B":["England","Iran","USA","Wales"],
          "C":["Argentina","Saudi Arabia","Mexico","Poland"],
          "D":["France", "Australia", "Denmark","Tunisia"],
          "E":["Spain", "Costa Rica", "Germany","Japan"],
          "F":["Belgium","Canada","Morocco","Croatia"],
          "G":["Brazil","Serbia","Switzerland","Cameroon"],
          "H":["Portugal","Ghana","Uruguay","South Korea"]}


Round16 = {49:{"A1":"","B2":""},
           50:{"C1":"","D2":""}, 
           51:{"B1":"","A2":""}, 
           52:{"D1":"","C2":""}, 
           53:{"E1":"","F2":""}, 
           54:{"G1":"","H2":""}, 
           55:{"F1":"","E2":""}, 
           56:{"H1":"","G2":""} 
           }

Quarters = {57:{49:"",50:""},
          58:{53:"",54:""},
          59:{51:"",52:""},
          60:{55:"",56:""}
        }

Semi =   {61:{57:"",58:""},
          62:{59:"",60:""}
        }

Thrird = {63:{61:"",62:""}}

Final  = {64:{61:"",62:""}}

ODDS_DATA = pd.read_csv("avg_odds_team.csv")
SCORE_DIST_WINNER = {0: 7,0.003: 8,0.006: 5,  0.012: 6, 0.131:4, 0.396:3, 0.676:2  }
SCORE_DIST_LOSER = { 0: 0, 0.5: 1, 0.9:2 }

def vlookupmatch(value, lookup_dict):
     lookup_list = sorted(lookup_dict)
     if value < lookup_list[0]:
         raise ValueError

     prev_lookup = None
     for lookup in lookup_list:
         if value < lookup:
             match = prev_lookup
             break
         else:
             prev_lookup = lookup
     else:
         match = lookup
     return lookup_dict[match]

def stronger_team(team1:tuple, team2:tuple)->tuple:
    team1_name, team1_odds = team1
    team2_name, team2_odds = team2
    return (team1,team2) if team1_odds < team2_odds else (team2,team1)


def match_teams(match:dict)->tuple:
    t1, t2 = match.values()
    return t1, t2

def match_result(match:tuple)->str:
    result = {}
    home_team, away_team = match
    
    home_team_odds = get_odds(home_team,ODDS_DATA)
    away_team_odds = get_odds(away_team,ODDS_DATA) 
    
    stronger_order = stronger_team((home_team,home_team_odds), (away_team, away_team_odds ))

    winner, loser = stronger_order 

    winner_name, winner_odds = winner
    loser_name, loser_odds = loser

    score_winner = vlookupmatch(random(), SCORE_DIST_WINNER)
    score_looser = vlookupmatch(random(), SCORE_DIST_LOSER)
    result[winner_name] = score_winner
    result[loser_name] = score_looser
    return result
    

def get_odds(team:str,odds:pd.DataFrame)->float:
    return odds[odds["team"]==team]["value"].values[0]

def group_matches(group_teams:list)->list:
    return list(combinations(group_teams,2))

def process_winner(result:dict)->str:
    winner = ""
    score = 0
    for team, goals in result.items():
        if goals == score:
            winner = "draw"
        if goals > score:
            winner = team
            score = goals
    return winner

def play_group(group:str, group_teams:list)->list:
    matches = group_matches(group_teams)
    points = defaultdict(list)
    goals = defaultdict(list)
    for match in matches:
        result = match_result(match)
        winner = process_winner(result)
        team1, team2 = match
        goals[team1].append(result[team1])
        goals[team2].append(result[team2])
        if winner == "draw":
            points[team1].append(1)
            points[team2].append(1)
        else:
            points[winner].append(3)
    points_totals = { k:sum(v) for k,v in points.items()}
    goals_totals = { k:sum(v) for k,v in goals.items()}

    through_teams = (sorted(points_totals.items(), key=lambda item: item[1], reverse=True)[:2])
    (team1,points1), (team2,points2) = through_teams

    group_result = [team1, team2]

    if points1 != points2:
        group_result = [team1, team2]
    
    if goals_totals[team1] > goals_totals[team1]:
        group_result = [team1, team2]
    
    if goals_totals[team2] > goals_totals[team1]:
        group_result = [team2, team1]

    if goals_totals[team2] == goals_totals[team1]:
        group_result = [team1, team2]

    return group , group_result

def group_stage(groups):
    group_stage_results = []
    for group, teams in groups.items():
        group_stage_results.append(play_group(group,teams))
    return group_stage_results


def round_16_populate(fixture,group_stage_results):
    for result in group_stage_results:
        current_group, through_teams = result
        for game, match in fixture.items():
            for team in match.keys():
                team_group, position = team[0], int(team[1])
                if team_group == current_group:
                    fixture[game][f"{team_group}{position}"] = through_teams[position - 1]
    return fixture


def round_16_results(round_16_matches):
    result = {}
    for match, game in round_16_matches.items():
        match_score =  match_result(match_teams(game))
        winner = process_winner(match_score)
        random_winner = choice(match_teams(game))
        result[match] = winner if winner != "draw" else random_winner

    return result

def quarters_populate(fixture,round_16_game_results):
    for game, match in fixture.items():
            for team in match.keys():
                fixture[game][team] = round_16_game_results[team]
    return fixture


def quarter_results(quarters_matches):
    result = {}
    for match, game in quarters_matches.items():
        match_score =  match_result(match_teams(game))
        winner = process_winner(match_score)
        random_winner = choice(match_teams(game))
        result[match] = winner if winner != "draw" else random_winner
    return result


def semi_populate(fixture,quarter_game_results):
    for game, match in fixture.items():
            for team in match.keys():
                fixture[game][team] = quarter_game_results[team]
    return fixture


def semi_results(semi_matches):
    final = {}
    third = {}
    for match, game in semi_matches.items():
        match_score =  match_result(match_teams(game))
        winner = process_winner(match_score)
        random_winner = choice(match_teams(game))
        definitive_winner = winner if winner != "draw" else random_winner
        final[match] = definitive_winner
        loser = [team for team in match_teams(game) if team != definitive_winner][0]
        third[match] = loser
    return final, third


def champion(final):
    match_score =  match_result(match_teams(final))
    winner = process_winner(match_score)
    random_winner = choice(match_teams(final))
    definitive_winner = winner if winner != "draw" else random_winner
    return definitive_winner


def third_place(third):
    match_score =  match_result(match_teams(third))
    winner = process_winner(match_score)
    random_winner = choice(match_teams(third))
    definitive_winner = winner if winner != "draw" else random_winner
    return definitive_winner

def simulate(nruns:int)->list:
    runs = []
    for i in range(nruns):
        run = {}
        group_stage_results = group_stage(Groups)
        run["group_stage_results"] = group_stage_results
        round_16_matches = round_16_populate(Round16,group_stage_results)
        run["round_16_matches"] = round_16_matches
        round_16_results_ = round_16_results(round_16_matches)
        quarters_matches = quarters_populate(Quarters,round_16_results_)
        run["quarter_matches"] = quarters_matches
        quarter_game_results = quarter_results(quarters_matches)
        run["quarter_game_results"] = quarter_game_results
        semi_matches = semi_populate(Semi, quarter_game_results)
        run["semi_matches"] = semi_matches
        final, third = semi_results(semi_matches)
        run["final"] = final
        run["champion"] = champion(final)
        run["third"] = third
        run["third_place"] = third_place(third)
        runs.append(run)
    return runs

simulations = simulate(1)

print(simulations)

champion_sim = [simulation["champion"]for simulation in simulations]

print(Counter(champion_sim))






