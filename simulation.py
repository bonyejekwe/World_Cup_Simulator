
import numpy as np
import pandas as pd
from itertools import combinations
from collections import Counter

# TODO: need to fix model predicting the goals for each game

class Simulation:

    def __init__(self, year, groups_list, pred_model, match_data) -> None:
        self.year = year
        self.model = pred_model
        self.data = match_data
        self.groups_list = groups_list  # list for that year

        self.team_ranks = {}
        self.team_scores = {}
        self.get_ranks_and_scores()

        self.win_avg = match_data[match_data["result"] == 1]['team_score'].mean()
        self.loss_avg = match_data[match_data["result"] == -1]['team_score'].mean()
        self.draw_avg = match_data[match_data["result"] == 0]['team_score'].mean()

    def get_ranks_and_scores(self):
        """Get the ranks and scores for each team and store in respective dictionaries"""
        for group in self.groups_list:
            for team in group:
                self.team_ranks[team] = self.data[self.data["team"] == team].iloc[-1]["team_rank"]
                self.team_scores[team] = self.data[self.data["team"] == team].iloc[-1]["team_points"]
     
    def get_probabs(self, team1, team2):
        """Get the probabilities"""
        rank1, rank2 = self.team_ranks[team1], self.team_ranks[team2]
        points1, points2 = self.team_scores[team1], self.team_scores[team2]
        
        rank_diff = rank1 - rank2
        avg_rank = (rank1 + rank2) / 2

        cols = ['rank_diff', 'avg_rank', 'neutral', 'team_points', 'opponent_points']
        row = pd.DataFrame(np.array([[rank_diff, avg_rank, True, points1, points2]]), columns=cols)
        team1_prob = round(self.model.predict_proba(row)[:,1][0], 2)   # probablity team1 wins

        row = pd.DataFrame(np.array([[-1 * rank_diff, avg_rank, True, points2, points1]]), columns=cols)
        team2_prob = round(self.model.predict_proba(row)[:,1][0], 2)   # probablity team2 wins

        tie_prob = 1 - team1_prob - team2_prob # probability of a tie
        return [team1_prob, tie_prob, team2_prob]

    def get_poisson_score(self, result, team1_avg, team2_avg):
        score1, score2 = np.random.poisson(team1_avg), np.random.poisson(team2_avg)

        if (result == 1) and (score1 <= score2):
            return self.get_poisson_score(result, team1_avg, team2_avg)
        elif (result == -1) and (score1 >= score2):
            return self.get_poisson_score(result, team1_avg, team2_avg)
        elif (result == 0) and (score1 != score2):  # result == 0
            return self.get_poisson_score(result, team1_avg, team2_avg)

        return score1, score2

    def get_poisson(self, result, rank1, rank2):
        th = 10  # within 5 of the rank
        d = self.data[(abs(self.data["team_rank"] - rank1) <= th) & (abs(self.data["opponent_rank"] - rank2) <= th) & (self.data["result"] == result)]
        return self.get_poisson_score(result, d["team_score"].mean(), d["opponent_score"].mean())
        
    def simulate_group_match(self, team1, team2, pr=False):
        """Simulate a group stage match between two teams. Returns result (-1, 0, or 1)"""
        trials = 1
        team1_prob, tie_prob, team2_prob = self.get_probabs(team1, team2)
        #result = Counter(np.random.choice([1, 0, -1], trials, p =[team1_prob, tie_prob, team2_prob]))
        #result = result.most_common()[0][0]  # either -1, 0, or 1
        result = np.random.choice([1, 0, -1], p = [team1_prob, tie_prob, team2_prob]) # either -1, 0, or 1 (1 trial)
        return result, team1_prob, tie_prob, team2_prob

    def simulate_group(self, group, pr=True):
        """Simulate a group or a matchup"""
        table_points = {team: 0 for team in group}
        gf = {team: 0 for team in group}
        ga = {team: 0 for team in group}
        draws = 0
        
        for team1, team2 in combinations(group, 2):  # each match
            rank1, rank2 = self.team_ranks[team1], self.team_ranks[team2]
            result, team1_prob, tie_prob, team2_prob = self.simulate_group_match(team1, team2)
            
            if result == 1: # team1 wins
                table_points[team1] += 3
                team1_goals, team2_goals = self.get_poisson(result, rank1, rank2)
                #win_goals, loss_goals = self.get_poisson(result, rank1, rank2) # np.random.poisson(self.win_avg), np.random.poisson(self.loss_avg)
                result_str = f"{team1_goals}-{team2_goals} {team1} beats {team2}:"
                gf[team1] += team1_goals
                gf[team2] += team2_goals
                ga[team1] += team1_goals
                ga[team2] += team2_goals

            elif result == -1: # team2 wins
                table_points[team2] += 3
                team1_goals, team2_goals = self.get_poisson(result, rank1, rank2)
                #win_goals, loss_goals = self.get_poisson(result, rank1, rank2) # np.random.poisson(self.win_avg), np.random.poisson(self.loss_avg)
                result_str = f"{team1_goals}-{team2_goals} {team1} loses to {team2}"
                gf[team1] += team1_goals
                gf[team2] += team2_goals
                ga[team1] += team1_goals
                ga[team2] += team2_goals
                ##gf[team1] += loss_goals
                #gf[team2] += win_goals
                #ga[team1] += win_goals
                #ga[team2] += loss_goals

            else: # result == 0 (tie)
                draws += 1
                table_points[team1] += 1
                table_points[team2] += 1
                team1_goals, team2_goals = self.get_poisson(result, rank1, rank2)
                #draw_goals = self.get_poisson(result, rank1, rank2)[0] # np.random.poisson(self.draw_avg)
                result_str = f"{team1_goals}-{team2_goals} {team1} draws {team2}"
                gf[team1] += team1_goals
                gf[team2] += team2_goals
                ga[team1] += team1_goals
                ga[team2] += team2_goals
                #gf[team1] += draw_goals
                #gf[team2] += draw_goals
                #ga[team1] += draw_goals
                #ga[team2] += draw_goals
                
            if pr:
                print(result_str, [round(team1_prob, 2), round(tie_prob, 2), round(team2_prob, 2)],  "-> ", result)

        gdiff = {team: gf[team] - ga[team] for team in group}
        standings = sorted(group, key=lambda x: (table_points[x], gdiff[x], gf[x]), reverse=True)
        standings = [(t, table_points[t], gdiff[t], gf[t]) for t in standings]
        
        if pr:
            print(standings, "draws:", draws)
        return standings

    def get_knockout_round(self, pr=True):
        """Get teams advancing to the knockout round"""
        gw = []  # group winners
        for group in self.groups_list:
            standings = [i[0] for i in self.simulate_group(group, pr=pr)]
            gw.append(standings[:2])
            
            if pr:
                print("")
        return gw

    def get_knockout_round_group(self, group, pr=True):
        """Get teams advancing to the knockout round"""
        return [i[0] for i in self.simulate_group(group, pr=pr)][:2]

    def simulate_knockout_match(self, team1, team2, pr=False):
        """Simulate a match between two teams. Returns the winning team"""
        trials = 1 #5
        team1_prob, tie_prob, team2_prob = self.get_probabs(team1, team2)

        result = Counter(np.random.choice([1, 0, -1], trials, p =[team1_prob, tie_prob, team2_prob]))
        result = result.most_common()[0][0]
        
        tie_str = ""
        if result == 0:  # no ties for knockout round
            total = team1_prob + team2_prob
            t1, t2 = team1_prob / total, team2_prob / total
            result = Counter(np.random.choice([1, -1], trials, p =[t1, t2])) 
            result = result.most_common()[0][0] # either 1 or -1
            tie_str = " in OT"
            
        if pr:
            if result == 1: # team1 wins
                print(f"{team1} beats {team2}{tie_str}: ".ljust(40), f"[{team1_prob} vs {team2_prob}]")
                
            else: # result == -1: # team2 wins
                print(f"{team1} loses to {team2}{tie_str}: ".ljust(40), f"[{team1_prob} vs {team2_prob}]")

        if result == 1:
            return team1
        else:
            return team2

    def simulate_knockout_round(self, gw, pr=False):
        """Simulate the knockout stages, determine top 4 teams"""
        r16 = [gw[0][0], gw[1][1], gw[2][0], gw[3][1], gw[4][0], gw[5][1], gw[6][0], gw[7][1],
            gw[1][0], gw[0][1], gw[3][0], gw[2][1], gw[5][0], gw[4][1], gw[7][0], gw[6][1]]

        if pr:
            print("Group Winners:", gw)
            print("\nR16: ", r16)

        qf = [self.simulate_knockout_match(r16[2*i], r16[2*i+1], pr=pr) for i in range(8)]

        if pr:
            print("\nQF : ", qf)

        sf = [self.simulate_knockout_match(qf[2*i], qf[2*i+1], pr=pr) for i in range(4)]
        
        if pr:
            print("\nSF : ", sf)

        final = [self.simulate_knockout_match(sf[2*i], sf[2*i+1], pr=pr) for i in range(2)]
        bronze = [t for t in sf if t not in final]
        
        if pr:
            print("\nB  :", bronze)
            print("F  :", final)
            
        third = self.simulate_knockout_match(bronze[0], bronze[1], pr=pr)
        fourth = [t for t in bronze if t != third][0]
        champ = self.simulate_knockout_match(final[0], final[1], pr=pr)
        second = [t for t in final if t != champ][0]
        return champ, second, third, fourth

