
import numpy as np
import pandas as pd
from itertools import combinations
from profiler import Profiler
from collections import Counter
from precompute import get_groups, get_teams, get_team_rank, get_team_score, all_pairings, compute_poission

opp_result = {3: 0, 1: 1, 0: 3}
str_result = {3: "beats", 1: "draws", 0: "loses to"}

class Match:

    def __init__(self, team1, team2, dist, poisson_dist) -> None:
        """Initialize a match object"""
        self.team1 = team1
        self.team2 = team2
        self.dist = dist
        self.poisson_dist = poisson_dist

    def simulate_match(self):
        """Simulate a match using the precomputed probability distribution"""
        team1_prob, tie_prob, team2_prob = self.dist[(self.team1, self.team2)]
        return np.random.choice([3, 1, 0], p = [team1_prob, tie_prob, team2_prob]) # result

    def get_match_score(self, result):
        """Return a possible score for the match given a result"""
        team1_avg, team2_avg = self.poisson_dist[(self.team1, self.team2)]
        score1, score2 = np.random.poisson(team1_avg), np.random.poisson(team2_avg)

        # if scores don't make sense with result, call function again
        if (result == 3) and (score1 <= score2):
            return self.get_match_score(result)
        elif (result == 0) and (score1 >= score2):
            return self.get_match_score(result)
        elif (result == 1) and (score1 != score2):
            return self.get_match_score(result)

        return score1, score2

    def probab_dist(self):
        """Return the probability distribution for the match [team1_prob, tie_prob, team2_prob]"""
        return self.dist[(self.team1, self.team2)]

    def get_error(self, result):
        """Get the "difference" between the randomly simulated result and the maximum likelihood result"""
        return 0
        l = self.dist[(self.team1, self.team2)]  # team1_prob, tie_prob, team2_prob
        if ((result == 1) and (max(l) == l[1])) or (result == 3) and (max(l) == l[0]) or (result == 0) and (max(l) == l[2]):
            return 0
        return 0
        if (result == 0) and (max(l) == l[1]):  # if tie most likely and predicted
            return 0
        elif (result == 0) or (max(l) == l[1]):  #
            return 1
        elif ((result == 1) and (max(l) == l[2])) or ((result == -1) and (max(l) == l[0])):
            return 3
        else:  # win most likely and predicted, or loss most likely and predicted
            return 0

 
class KnockoutMatch(Match):

    def __init__(self, team1, team2, dist, poisson_dist) -> None:
        super().__init__(team1, team2, dist, poisson_dist)

    def simulate_match(self):
        """Return the result (3 or 0) for the knockout match (no ties)"""
        #result = super().simulate_match()
        team1_prob, tie_prob, team2_prob = self.dist[(self.team1, self.team2)]
        result = np.random.choice([3, 1, 0], p = [team1_prob, tie_prob, team2_prob])
        #tie_str = ""
        if result == 1:  # no ties for knockout round
            t1, t2 = team1_prob / (team1_prob + team2_prob), team2_prob / (team1_prob + team2_prob)
            result = np.random.choice([3, 0], p=[t1, t2])
            #tie_str = " in OT" 
        return result

    def match_winner(self, pr=False):
        """Return the name of the winning team"""
        result = self.simulate_match()

        if pr:
            print(f"{self.team1} {str_result[result]} {self.team2}")

        if result == 3:
            return self.team1
        else:  # result == 0
            return self.team2


    def get_error(self, result):
        return 0
        l = self.dist[(self.team1, self.team2)]  # team1_prob, tie_prob, team2_prob
        if ((result == self.team1) and (l[0] > l[2])) or ((result == self.team2) and (l[2] > l[0])):
            return 0
        else: # add to error
            return 3

class Simulation:

    def __init__(self, year, pred_model, match_data) -> None:
        self.year = year
        self.model = pred_model
        self.data = match_data
        self.groups_list =  get_groups(year)  # list for that year
        self.teams = get_teams(self.groups_list)

        self.team_ranks = {t: get_team_rank(t, self.data) for t in self.teams}
        self.team_scores = {t: get_team_score(t, self.data) for t in self.teams}

        self.prob_dist = {}
        self.poissons = {}
        self.precompute_match_data()

        self.result = {}
        self.error = []

    def compute_probabs(self, team1, team2):
        """Get the probabilities for a match pairing"""
        rank1, rank2 = self.team_ranks[team1], self.team_ranks[team2]
        points1, points2 = self.team_scores[team1], self.team_scores[team2]
        cols = ['team_rank', "opponent_rank", 'team_points', 'opponent_points']
        
        row1 = pd.DataFrame(np.array([[rank1, rank2, points1, points2]]), columns=cols)
        team1_prob = round(self.model.predict_proba(row1)[:,1][0], 2)   # probablity team1 wins
        
        row2 = pd.DataFrame(np.array([[rank2, rank1, points2, points1]]), columns=cols)
        team2_prob = round(self.model.predict_proba(row2)[:,1][0], 2)   # probablity team2 wins

        return [team1_prob, 1 - team1_prob - team2_prob, team2_prob]  # team1_prob, tie_prob, team2_prob

    def precompute_match_data(self):
        """Precompute the data for each possible matchup (since are constant for an entire simulation"""
        for t1, t2 in all_pairings(self.teams):
            self.prob_dist[(t1, t2)] = self.compute_probabs(t1, t2)
            self.prob_dist[(t2, t1)] = self.compute_probabs(t2, t1)

            s1, s2 = compute_poission(self.team_ranks[t1], self.team_ranks[t2], self.data)
            self.poissons[(t1, t2)] = (s1, s2)
            self.poissons[(t2, t1)] = (s2, s1)
        return

    def get_probabs(self, team1, team2):
        """Get the probabilities"""
        return self.prob_dist[(team1, team2)]

    def get_poisson_avg(self, team1, team2):
        """Get the poisson avg for each team"""
        return self.poissons[(team1, team2)]

    @Profiler.profile
    def simulate_group(self, group, pr=False):
        """Simulate a group stage"""
        table_points = {team: 0 for team in group}
        gf = {team: 0 for team in group}
        ga = {team: 0 for team in group}
        draws = 0
        
        for team1, team2 in combinations(group, 2):  # each match
            m = Match(team1, team2, self.prob_dist, self.poissons)
            result = m.simulate_match()
            self.error.append(m.get_error(result))
            team1_goals, team2_goals = m.get_match_score(result)
            
            gf[team1] += team1_goals
            gf[team2] += team2_goals
            ga[team1] += team2_goals
            ga[team2] += team1_goals

            table_points[team1] += result
            table_points[team2] += opp_result[result]

            if result == 1: # tie
                draws += 1

            if pr:
                team1_prob, tie_prob, team2_prob = m.probab_dist()
                result_str = f"{team1_goals}-{team2_goals}: {team1} {str_result[result]} {team2}:"
                print(result_str, [round(team1_prob, 2), round(tie_prob, 2), round(team2_prob, 2)],  "-> ", result)

        gdiff = {team: gf[team] - ga[team] for team in group}
        standings = sorted(group, key=lambda x: (table_points[x], gdiff[x], gf[x]), reverse=True)[:2]
        
        if pr:
            full_standings = [(t, table_points[t], gdiff[t], gf[t]) for t in standings]
            print(full_standings, "draws:", draws)

        return standings

    @Profiler.profile
    def get_knockout_round(self, pr=True):
        """Get the teams advancing to the knockout round"""
        gw = [self.simulate_group(g, pr) for g in self.groups_list.values()]

        if pr:
            print("")

        self.result["groups"] = gw
        return gw

    #@Profiler.profile
    def get_knockout_round_group(self, group, pr=True):
        """Get teams advancing to the knockout round"""
        return [i for i in self.simulate_group(group, pr=pr)][:2]

    #@Profiler.profile
    def simulate_round(self, teams_lis, n_round="S", print_result=True):
        """NOTE: teams lis should be ordered properly"""
        next_round = []
        n = len(teams_lis)  # number in the next round
        num = int(n / 2)
        for i in range(num):
            m = KnockoutMatch(teams_lis[2*i], teams_lis[2*i+1], self.prob_dist, self.poissons)
            result = m.match_winner()  # get the winning team
            self.error.append(m.get_error(result))
            next_round.append(result)
        
        self.result[n_round] = next_round
        
        if print_result:
            print(f"{n_round}: {next_round}")
        return next_round

    @Profiler.profile
    def simulate_knockout_round(self, gw, pr=False):
        """Simulate the knockout stages, determine top 4 teams"""
        self.result = {}
        r16 = [gw[0][0], gw[1][1], gw[2][0], gw[3][1], gw[4][0], gw[5][1], gw[6][0], gw[7][1],
            gw[1][0], gw[0][1], gw[3][0], gw[2][1], gw[5][0], gw[4][1], gw[7][0], gw[6][1]]
        self.result["r16"] = r16

        if pr:
            print("Group Winners:", gw)
            print("\nR16: ", r16)

        qf = self.simulate_round(r16, "QF", pr)
        sf = self.simulate_round(qf, "SF", pr)
        final = self.simulate_round(sf, "final", False)

        bronze = [t for t in sf if t not in final]
        self.result["bronze"] = bronze
        
        if pr:
            print("B :", bronze)
            print("F :", final)
        
        third = self.simulate_round(bronze, "third", pr)[0]
        fourth = [t for t in bronze if t != third][0]
        champ = self.simulate_round(final, "champ", pr)[0]
        second = [t for t in final if t != champ][0]
        self.result["summary"] = [champ, second, third, fourth]
        self.result["error"] = self.error
        return champ, second, third, fourth

    def simulate_tournament(self, pr1=False, pr2=False):
        self.error = []
        gw = self.get_knockout_round(pr1)
        return self.simulate_knockout_round(gw, pr2)

    def get_result(self, res):
        """Get a result"""
        return self.result[res]

    def get_simulation_results(self, iterations):
        """Run {iterations} simulations and return a list of the results"""
        results_list = []
        for i in range(iterations):
            self.simulate_tournament(False, False)
            results_list.append(self.result)
            #if i % p == 0:
            #    print(f"{(i / iters)*100}% done")
        return results_list


from get_match_data import *
from prediction_model import get_model

@Profiler.profile
def main():
    errors = []
    YEAR = 2022  # year for the model
    rankings, data = get_data(YEAR)
    logreg, match_data = get_model(data, report=True)

    s = Simulation(YEAR, logreg, match_data)
    for _ in range(1000):
        r = s.simulate_tournament(False, False)
        errors.append(sum(s.error))


if __name__ == "__main__":
    main()
    print(Profiler.report())