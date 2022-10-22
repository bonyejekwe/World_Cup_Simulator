
# functions to precompute information
import json

def get_groups(year, filename="group_stages.json") -> dict:
    """Get the group stages dictionary {group_letter: teams} for specified year"""
    with open(filename, "r") as file:
        d = json.load(file)
    return d[str(year)]

def get_teams(groups_list):
    """Return the teams as a single list"""
    teams = []
    for group in groups_list.values():
        teams += group
    return teams

def get_team_rank(team, data):
    """Get the rank of a team given the data (which should be year-restricted"""
    return data[data["team"] == team].iloc[-1]["team_rank"]

def get_team_score(team, data):
    """Get the ELO score of a team given the data (which should be year-restricted"""
    return data[data["team"] == team].iloc[-1]["team_points"]

def all_pairings(teams):
    """Helper function to get list of all pairings"""
    team_pairings = []
    for t1 in teams:
        for t2 in teams:
            if t1 != t2:
                team_pairings.append((t1, t2))
    return team_pairings


####
def compute_poission(rank1, rank2, data, th=10):
    """Compute the mean goals scored in matchups with similar rankings"""
    d = data[(abs(data["team_rank"] - rank1) <= th) & (abs(data["opponent_rank"] - rank2) <= th)]# & (self.data["result"] == result)]
    return d["team_score"].mean(), d["opponent_score"].mean()