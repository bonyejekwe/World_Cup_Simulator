
from collections import Counter
from get_match_data import *
from group_stages import *
from prediction_model import get_model
from simulation import *

YEAR = 2018  # year for the model
rankings, data = get_data(YEAR)

logreg, match_data = get_model(data, report=False)
sf_counter = Counter()

def evals(iters):
    p = int(iters / 5)
    results_dict = []
    s = Simulation(YEAR, groups_list[YEAR], logreg, match_data)
    for i in range(iters):
        s.simulate_knockout_round(s.get_knockout_round(False), pr=False)
        results_dict.append(s.result)
        if i % p == 0:
            print(f"{(i / iters)*100}% done")
    print("done")
    return results_dict


def compare_win(teams, results, iters):
    """Compare the probability of winning the World Cupfor each team"""
    for team in teams:
        filtered = [r for r in results if team in r['r16']]
    pass

def compare_win_from_knockout(teams, results, iters):
    """Compare the probability of winning the World Cupfor each team,
    given that the team made the knockout stages"""
    for team in teams:
        filtered = [r for r in results if team in r['r16']]
        wins = len([r for r in filtered if team == r['summary'][0]])
        num, den = wins, len(filtered)
    pass


def knockout_round_vs_win(results, team):
    filtered = [r for r in results if team in r['r16']]
    filtered2 = [r for r in filtered if team == r['summary'][0]] #team in r['sf']] #team == r['summary'][0]]
    num, den = len(filtered2), len(filtered)
    if den > 0:
        #print(f"{team}:, {num} / {den} = {round(num / den, 2)}")
        return num / den
    else:
        #print(f"{team}:, {num} / {den} = {round(0, 2)}")
        return 0

def win(results, team):
    #return len([r for r in results if team in r['sf']]) / iterats
    return len([r for r in results if team == r['summary'][0]]) / iterats


iterats = 1000
res = evals(iterats)
s = Simulation(YEAR, groups_list[YEAR], logreg, match_data)
tm_lis = [(tm, round(knockout_round_vs_win(res, tm), 3), round(win(res, tm), 3)) for tm in s.teams]
print('h')

tm_lis = sorted(tm_lis, key=lambda x: x[1], reverse=True)#[:10]
for tup in tm_lis:
    print(tup)


tm_lis = [(tm, round(knockout_round_vs_win(res, tm) - win(res, tm), 3)) for tm in s.teams]

print('h')

tm_lis = sorted(tm_lis, key=lambda x: x[1], reverse=True)#[:10]
for tup in tm_lis:
    print(tup)