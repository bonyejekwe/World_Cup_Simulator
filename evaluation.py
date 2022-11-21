
import pandas as pd
from collections import Counter

def convert_to_groups(r16):
    """Convert a r16 list to the group winners matrix"""
    gw =[[r16[0], r16[9]], [r16[8], r16[1]], [r16[2], r16[11]], [r16[10], r16[3]],
         [r16[4], r16[13]], [r16[12], r16[5]], [r16[6], r16[15]], [r16[14], r16[7]]]
    return gw

def common_winners(results, year):
    """Return a counter for the most common tournament winners from a list of iterations"""
    winners = [ res['champ'][0] for res in results ]
    c = Counter(winners).most_common(10)

    print(f"Most common winners of {year} World Cup...")
    for team, num in c:
        print(f"{team}: {round((num / len(results)) * 100, 1)}%")

def team_makes_round(results, team, round1):
    """Returns the % of times a team makes {round}"""
    return len([res for res in results if team in res[round1]]) / len(results)

def get_prob_df(results, groups_list):
    """Return a dataframe for probabilities of all teams in all rounds"""
    data = []
    for group in groups_list:
        for team in group:
            pw = round(100 * team_makes_round(results, team, "champ"), 4)
            pf = round(100 * team_makes_round(results, team, "final"), 4)
            ps = round(100 * team_makes_round(results, team, "SF"), 4)
            pq = round(100 * team_makes_round(results, team, "QF"), 4)
            pr = round(100 * team_makes_round(results, team, "r16"), 4)
            data.append([team, pr, pq, ps, pf, pw])
    
    return pd.DataFrame(data, columns=["team", "r16", "QF", "SF", "final", "champ"])


# to be used

def team_between_rounds(results, team, round1, round2):
    """Returns the % of times a team makes {round2} given that they made {round1"""
    p1 = team_makes_round(results, team, round1)
    p2 = team_makes_round(results, team, round2)
    return p2 / p1


def common_teams_in_round(results, round1, year, num=10):
    """Most common teams in that round"""
    rounds = [ frozenset(res[round1]) for res in results ] # set for each simulated round 
    c = Counter(rounds).most_common(num)

    print(f"Most common {round1} occurences at {year} World Cup...")
    for team, prop in c:
        print(f"{list(team)}: {round((prop / len(results)) * 100, 1)}%")


def group_progression(results, group_num):
    """Get the probabilities for the top two progressing teams of a group (in order)"""
    # group_num = {0: 'a', 1: 'b', ...}
    advancing = {}
    for result in results:
        top_two = tuple(convert_to_groups(result["r16"])[group_num])
        if top_two in advancing.keys():
            advancing[top_two] += 1
        else:
            advancing[top_two] = 1
    
    print("Most common advancing pair (in order)")
    for team, num in sorted(advancing.items(), key=lambda x:x[1], reverse=True):
        print(f"{team}: {round((num / len(results)) * 100, 1)}%")


def group_winners(results, group_num):
    """Get the probabilities for the winner of a group"""
    # group_num = {0: 'a', 1: 'b', ...}
    group_winners = {}
    for result in results:
        winner = convert_to_groups(result["r16"])[group_num][0]
        if winner in group_winners.keys():
            group_winners[winner] += 1
        else:
            group_winners[winner] = 1
    
    print("Most common group winners")
    for team, num in sorted(group_winners.items(), key=lambda x:x[1], reverse=True):
        print(f"{team}: {round((num / len(results)) * 100, 1)}%")


# not used
def most_similar(results, year, iterations, cap):
    # TODO compute "error" for each simulation
    """Used to determiner similarity based on error"""
    print(Counter([sum(res['error']) for res in results]))
    print(common_winners(year, iterations, results))
    
    results1 = results[:cap]
    results2 = sorted(results, key=lambda x: abs(54 - sum(x['error'])))[:cap]
    print(common_winners(year, cap, results1))
    print(common_winners(year, cap, results2))


def main():
    most_similar(2018, iterations=30000, cap=10000)

if __name__ == "__main__":
    main()