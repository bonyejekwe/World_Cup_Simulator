import re
import numpy as np
import pandas as pd


def read_match_data():
    """Return match data read in from csv"""
    # https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017 (downloaded 11/19/22)
    matches = pd.read_csv("data/match_results.csv")
    matches['date'] = pd.to_datetime(matches["date"])
    matches["year"] = [date.year for date in matches["date"]]  # [(i.year, i.month, i.day) for i in matches["date"]]
    return matches


def duplicate_matches(data):
    """duplicate the dataset so every game is represented twice (home/away -> team/opponent)"""
    # duplic = data.copy()
    d1, d2 = data.copy(), data.copy()

    d1 = d1.rename(columns={"home_team": "team", "away_team": "opponent", "home_score": "team_score", "away_score": "opponent_score"})
    d2 = d2.rename(columns={"away_team": "team", "home_team": "opponent", "away_score": "team_score", "home_score": "opponent_score"})
    duplic = pd.concat([d1, d2])
    return duplic


def get_elo_rankings(start, end):
    """Get ELO rankings and scores for teams from a given time frame
        ex: start_date = '2010-1-1', end_date='2010-12-31'."""
    start, end = pd.to_datetime(start), pd.to_datetime(end)
    s_day, s_mon, s_yr = str(start.day).zfill(2), str(start.month).zfill(2), start.year
    e_day, e_mon, e_yr = str(end.day).zfill(2), str(end.month).zfill(2), end.year

    link = f"https://www.international-football.net/average-elo-ratings?init=1&start-year={s_yr}&start-month={s_mon}&start-day={s_day}&end-year={e_yr}&end-month={e_mon}&end-day={e_day}&type=day"
    df = pd.read_html(link)
    df = pd.concat(df)

    df["Rank"] = df[0]
    df["Team"] = [re.split('\d', row)[0] for row in df[2]]
    df["Score"] = df[3]
    df["Year"] = e_yr
    df = df[["Rank", "Team", "Score", "Year"]]
    return df


def wc_rankings(start, end):
    """Get all rankings from start date to end date"""
    start, end = pd.to_datetime(start), pd.to_datetime(end)
    s_day, s_mon, s_yr = str(start.day).zfill(2), str(start.month).zfill(2), start.year
    e_day, e_mon, e_yr = str(end.day).zfill(2), str(end.month).zfill(2), end.year

    years = []
    years.append(get_elo_rankings(f"{s_yr}-{s_mon}-{s_day}", f"{s_yr}-12-31"))
    years += [get_elo_rankings(f"{yr}-01-01", f"{yr}-12-31") for yr in range(s_yr + 1, e_yr)]
    years.append(get_elo_rankings(f"{e_yr}-01-01", f"{e_yr}-{e_mon}-{e_day}"))
    return pd.concat(years)


def get_data(year):
    """Get the data up to {year}"""
    rankings = pd.read_csv(ranking_year[year]) # = wc_rankings("1998-01-01", wc_start[year])

    data = duplicate_matches(read_match_data())
    data = data.merge(rankings, left_on=["team", "year"], right_on=["Team", "Year"]).rename(
        columns={"Rank": "team_rank", "Score": "team_points"}).drop(columns=["Team", "Year"])
    data = data.merge(rankings, left_on=["opponent", "year"], right_on=["Team", "Year"]).rename(
        columns={"Rank": "opponent_rank", "Score": "opponent_points"}).drop(columns=["Team", "Year"])

    data = data[data['tournament'] != "Friendly"]
    data['rank_diff'] = data['team_rank'] - data['opponent_rank']
    data['avg_rank'] = (data['team_rank'] + data['opponent_rank']) / 2
    data['score_diff'] = data['team_score'] - data['opponent_score']
    data['team_won'] = data['score_diff'] > 0
    data['result'] = np.sign(
        data['team_score'] - data['opponent_score'])  # -1 if home lost, 1 if home win, and 0 if tie
    data['comp'] = data['tournament'] == "FIFA World Cup"
    return rankings, data


wc_start = {2022: "2022-11-21", 2018: "2018-06-14", 2014: "2014-06-12", 2010: "2010-06-11"}
ranking_year = {2022: "data/rankings22.csv", 2018: "data/rankings18.csv", 2014: "data/rankings14.csv", 2010: "data/rankings10.csv"}
# NOTE: 2022 ranking data is hardcoded for when last saved to csv (Nov 11)
