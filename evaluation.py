
from collections import Counter
from get_match_data import wc_rankings, wc_start, get_data
from precompute import get_groups
from prediction_model import get_model
from simulation import Simulation

def convert_to_groups(r16):
    """Convert a r16 list to the group winners matrix"""
    gw =[[r16[0], r16[9]], [r16[8], r16[1]],
         [r16[2], r16[11]], [r16[10], r16[3]],
         [r16[4], r16[13]], [r16[12], r16[5]],
         [r16[6], r16[15]], [r16[14], r16[7]]]
    return gw

def get_sim_results(year, iterations):
    """Get the results of {iterations} simulations"""
    rankings, data = get_data(year)
    logreg, match_data = get_model(data, report=False)
    s = Simulation(year, logreg, match_data)

    results_list = []
    for i in range(iterations):
        s.simulate_tournament(False, False)
        results_list.append(s.result)
        #if i % p == 0:
        #    print(f"{(i / iters)*100}% done")
    return results_list

def common_winners(year, iterations, results=None):
    """Results is optional, can be passed in"""
    if not results:
        results = get_sim_results(year, iterations)

    winners = [ res['champ'][0] for res in results ]
    c = Counter(winners).most_common(10)

    print(f"Most common winners of {year} World Cup...")
    for team, num in c:
        print(f"{team}: {round((num / iterations) * 100, 1)}%")

def team_wins(team, year, iterations, results= None):
    """Returns the % of times a team wins the tournament"""
    return team_makes_round(team, "champ", year, iterations)

def team_makes_round(team, round1, year, iterations, results=None):
    """Returns the % of times a team makes {round}"""
    if not results:
        results = get_sim_results(year, iterations)
    
    return len([res for res in results if team in res[round1]]) / iterations

def team_between_rounds(team, round1, round2, year, iterations, results=None):
    """Returns the % of times a team makes {round2} given that they made {round1"""
    pass

def common_round(round1, year, iterations, results=None):
    """Results is optional, can be passed in"""
    if not results:
        results = get_sim_results(year, iterations)

    winners = [ frozenset(res[round1]) for res in results ]
    c = Counter(winners).most_common(10)

    print(f"Most common {round1} occurences at {year} World Cup...")
    for team, num in c:
        print(f"{list(team)}: {round((num / iterations) * 100, 1)}%")

#def compare_between_rounds()

#common_winners(2018, 1000)
import pandas as pd

def get_prob_df(year, iterations, results=None):
    if not results:
        results = get_sim_results(year, iterations)

    data = []
    for group in get_groups(year).values():
        for team in group:
            pw = round(100 * team_makes_round(team, "champ", year, iterations, results), 4)
            pf = round(100 * team_makes_round(team, "final", year, iterations, results), 4)
            ps = round(100 * team_makes_round(team, "sf", year, iterations, results), 4)
            pq = round(100 * team_makes_round(team, "qf", year, iterations, results), 4)
            pr = round(100 * team_makes_round(team, "r16", year, iterations, results), 4)
            data.append([team, pr, pq, ps, pf, pw])
    
    return pd.DataFrame(data, columns=["team", "r16", "qf", "sf", "final", "champ"])

#df = get_prob_df(2018, 10000)
#print(df)

#common_round("champ", 2018, 1000)
#common_round("r16", 2018, 1000)


# TODO compute log likelihood for each simulation

def most_similar(year, iterations, cap, results=None):
    if not results:
        results = get_sim_results(year, iterations)

    print(Counter([sum(res['error']) for res in results]))
    print()
    print(common_winners(year, iterations, results))
    print()
    
    #print(Counter([r['champ'][0] for r in results[:cap]]))
    results1 = results[:cap]
    results2 = sorted(results, key=lambda x: abs(54 - sum(x['error'])))[:cap]

    print(common_winners(year, cap, results1))
    print()
    print(common_winners(year, cap, results2))


def main():
    most_similar(2018, iterations=30000, cap=10000)

if __name__ == "__main__":
    main()