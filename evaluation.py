
from collections import Counter
from get_match_data import *
from group_stages import *
from prediction_model import get_model
from simulation import *
import json

# TODO take into account previous years of rankings in the logreg model

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


def comparison():
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



def real_result():

    pass

iterats = 1000


s = Simulation(YEAR, groups_list[YEAR], logreg, match_data)
s.simulate_knockout_round(s.get_knockout_round(False), pr=False)
predicted_result = s.result
print("P: ", predicted_result)


result_d = {2022: "results/result22.json", 2018: "results/result18.json", 2014: "results/result14.json", 2010: "results/result10.json"}

with open(result_d[YEAR], "r") as f:
    actual_results = json.load(f)

print("A: ", actual_results)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


counts = {'r16': [], 'qf': [], 'sf': [], 'final': []}

print("I")

def conv(l):
    g =[[l[0], l[9]],
        [l[8], l[1]],
        [l[2], l[11]],
        [l[10], l[3]],
        [l[4], l[13]],
        [l[12], l[5]],
        [l[6], l[15]],
        [l[14], l[7]]]
    return g


#r16 = [gw[0][0], gw[1][1], gw[2][0], gw[3][1], gw[4][0], gw[5][1], gw[6][0], gw[7][1],
#            gw[1][0], gw[0][1], gw[3][0], gw[2][1], gw[5][0], gw[4][1], gw[7][0], gw[6][1]]

for _ in range(10000):
    for st in ['r16', 'qf', 'sf', 'final']:
        s.simulate_knockout_round(conv(actual_results['r16']), pr=False)
        #s.simulate_knockout_round(s.get_knockout_round(False), pr=False)
        predicted_result = s.result
        #print(st, len(intersection(actual_results[st], predicted_result[st])), intersection(actual_results[st], predicted_result[st]))
        counts[st].append(len(intersection(actual_results[st], predicted_result[st])))
        #if st == "r16" and len(intersection(actual_results[st], predicted_result[st])) != 16:
        #    break


for k, lis in counts.items():
    print(k, round(sum(lis) / len(lis), 3))
    print(Counter(lis))