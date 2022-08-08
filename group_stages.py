# 2010 World Cup Groups
group_a10 = ["Uruguay", "Mexico", "South Africa", "France"]
group_b10 = ["Argentina", "South Korea", "Greece", "Nigeria"]
group_c10 = ["United States", "England", "Slovenia", "Algeria"]
group_d10 = ["Germany", "Ghana", "Australia", "Serbia"]
group_e10 = ["Netherlands", "Japan", "Denmark", "Cameroon"]
group_f10 = ["Paraguay", "Slovakia", "New Zealand", "Italy"]
group_g10 = ["Brazil", "Portugal", "Ivory Coast", "North Korea"]
group_h10 = ["Spain", "Chile", "Switzerland", "Honduras"]

# 2014 World Cup Groups
group_a14 = ["Brazil", "Mexico", "Croatia", "Cameroon"]
group_b14 = ["Netherlands", "Chile", "Spain", "Australia"]
group_c14 = ["Colombia", "Greece", "Ivory Coast", "Japan"]
group_d14 = ["Costa Rica", "Uruguay", "Italy", "England"]
group_e14 = ["France", "Switzerland", "Ecuador", "Honduras"]
group_f14 = ["Argentina", "Nigeria", "Bosnia and Herzegovina", "Iran"]
group_g14 = ["Germany", "United States", "Portugal", "Ghana"]
group_h14 = ["Belgium", "Algeria", "Russia", "South Korea"]

# 2018 World Cup Groups
group_a18 = ["Uruguay", "Russia", "Saudi Arabia", "Egypt"]
group_b18 = ["Spain", "Portugal", "Iran", "Morocco"]
group_c18 = ["France", "Denmark", "Peru", "Australia"]
group_d18 = ["Croatia", "Argentina", "Nigeria", "Iceland"]
group_e18 = ["Brazil", "Switzerland", "Serbia", "Costa Rica"]
group_f18 = ["Sweden", "Mexico", "South Korea", "Germany"]
group_g18 = ["Belgium", "England", "Tunisia", "Panama"]
group_h18 = ["Colombia", "Japan", "Senegal", "Poland"]

# 2022 World Cup Groups
group_a22 = ["Qatar", "Ecuador", "Senegal", "Netherlands"]
group_b22 = ["England", "Iran", "United States", "Wales"]
group_c22 = ["Argentina", "Saudi Arabia", "Mexico", "Poland"]
group_d22 = ["France", "Australia", "Denmark", "Tunisia"]
group_e22 = ["Spain", "Costa Rica", "Germany", "Japan"]
group_f22 = ["Belgium", "Canada", "Morocco", "Croatia"]
group_g22 = ["Brazil", "Serbia", "Switzerland", "Cameroon"]
group_h22 = ["Portugal", "Ghana", "Uruguay", "South Korea"]

groups_list10 = [group_a10, group_b10, group_c10, group_d10, group_e10, group_f10, group_g10, group_h10]
groups_list14 = [group_a14, group_b14, group_c14, group_d14, group_e14, group_f14, group_g14, group_h14]
groups_list18 = [group_a18, group_b18, group_c18, group_d18, group_e18, group_f18, group_g18, group_h18]
groups_list22 = [group_a22, group_b22, group_c22, group_d22, group_e22, group_f22, group_g22, group_h22]
groups_list = {2022: groups_list22, 2018: groups_list18, 2014: groups_list14, 2010: groups_list10}


# for i in range(len(all_teams18)):
#   team = all_teams18[i]
#    print(i, team, list(rankings[rankings["Team"] == team]["Year"])[-1])

# for i in range(len(all_teams22)):
#    team = all_teams22[i]
#   print(i, team, matches[(matches["home_team"] == team) | (matches["away_team"] == team)].shape[0])
