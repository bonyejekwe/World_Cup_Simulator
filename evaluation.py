
import pandas as pd
from collections import Counter

def convert_to_groups(r16):
    """Convert a r16 list to the group winners matrix"""
    gw =[[r16[0], r16[9]], [r16[8], r16[1]], [r16[2], r16[11]], [r16[10], r16[3]],
         [r16[4], r16[13]], [r16[12], r16[5]], [r16[6], r16[15]], [r16[14], r16[7]]]
    return gw

def common_winners(results, year, iterations):
    """Return a counter for the most common tournament winners from a list of iterations"""
    winners = [ res['champ'][0] for res in results ]
    c = Counter(winners).most_common(10)

    print(f"Most common winners of {year} World Cup...")
    for team, num in c:
        print(f"{team}: {round((num / iterations) * 100, 1)}%")

def team_makes_round(results, team, round1, iterations):
    """Returns the % of times a team makes {round}"""
    return len([res for res in results if team in res[round1]]) / iterations

def get_prob_df(results, groups_list, iterations):
    """Return a dataframe for probabilities of all teams in all rounds"""
    data = []
    for group in groups_list:
        for team in group:
            pw = round(100 * team_makes_round(results, team, "champ", iterations), 4)
            pf = round(100 * team_makes_round(results, team, "final", iterations), 4)
            ps = round(100 * team_makes_round(results, team, "SF", iterations), 4)
            pq = round(100 * team_makes_round(results, team, "QF", iterations), 4)
            pr = round(100 * team_makes_round(results, team, "r16", iterations), 4)
            data.append([team, pr, pq, ps, pf, pw])
    
    return pd.DataFrame(data, columns=["team", "r16", "QF", "SF", "final", "champ"])

# not used

def team_wins(team, year, iterations, results= None):
    """Returns the % of times a team wins the tournament"""
    return team_makes_round(team, "champ", year, iterations)


def team_between_rounds(team, round1, round2, year, iterations, results=None):
    """Returns the % of times a team makes {round2} given that they made {round1"""
    pass

def common_round(results, round1, year, iterations):
    """Results is optional, can be passed in"""
    winners = [ frozenset(res[round1]) for res in results ]
    c = Counter(winners).most_common(10)

    print(f"Most common {round1} occurences at {year} World Cup...")
    for team, num in c:
        print(f"{list(team)}: {round((num / iterations) * 100, 1)}%")


# TODO compute log likelihood for each simulation

def most_similar(results, year, iterations, cap):
    """Used to determiner similarity based on error"""
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