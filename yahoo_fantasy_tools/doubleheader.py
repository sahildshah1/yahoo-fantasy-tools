"""
Compute  "doubleheader" standings for the current week of the season
"""

import statistics
import shelve
import itertools
from collections import Counter

import pandas as pd
import click
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa


def get_alternative_standings(lg):
    """ Compute "doubleheader" standings

    Parameters
    ----------
    lg : yahoo_fantasy_api.League
        An instance of the yahoo_fantasy_api League class

    Returns
    --------
    pandas.DataFrame

    """

    standings = get_current_standings(lg)
    bonus_wins = get_bonus_wins()

    # Add team names to data frame
    teams = lg.teams()

    df = pd.DataFrame(
        {
            "team_key": list(standings.keys()),
            "team_name": [teams[key]["name"] for key in standings.keys()],
            "wins": [int(val["wins"]) for val in standings.values()],
            "bonus_wins": [bonus_wins[key] for key in standings.keys()],
        }
    )

    df["total_wins"] = df["wins"] + df["bonus_wins"]
    df["ties"] = [int(val["ties"]) for val in standings.values()]

    df = df.sort_values(by=["total_wins"], ascending=False, ignore_index=True)

    return df


def get_current_standings(lg):
    """ Get current outcome totals 

    Parameters
    ----------
    lg : yahoo_fantasy_api.League
        An instance of the yahoo_fantasy_api League class

    Returns
    -------
    dict 

    """

    standings = lg.standings()

    return {team["team_key"]: team["outcome_totals"] for team in standings}


def get_bonus_wins():
    """ Get bonus wins 

    Returns
    -------
    collections.Counter
        An instance of the collections.Counter class

    """

    with shelve.open("fantasy_points") as db:
        top_half_teams = [get_top_half_teams(db[key]) for key in db]

    # Flatten list of sets
    top_half_teams = list(itertools.chain(*top_half_teams))

    return Counter(top_half_teams)


def get_top_half_teams(points):
    """ Get top half teams

    Parameters
    ----------
    points : dict
        The key value pairs are {"team_key": "points"}

    Returns
    -------
    set 

    """

    median_points = statistics.median(
        [float(points) for points in list(points.values())]
    )

    return {team for team, points in points.items() if float(points) > median_points}


def get_current_points(lg):
    """ Get current points

    Parameters
    ----------
    lg : yahoo_fantasy_api.League
        An instance of the yahoo_fantasy_api League object

    Returns
    ---------
    dict 

    """

    matchups_content = lg.matchups()

    matchups = matchups_content["fantasy_content"]["league"][1]["scoreboard"]["0"][
        "matchups"
    ]

    points = {}

    for matchup in range(matchups["count"]):

        teams = matchups[str(matchup)]["matchup"]["0"]["teams"]

        for team in range(teams["count"]):

            team_key = teams[str(team)]["team"][0][0]["team_key"]
            team_points = teams[str(team)]["team"][1]["team_points"]["total"]

            points[team_key] = team_points

    return points


@click.command()
@click.option("-league_id", help="League ID")
@click.option("--shelf", is_flag=True)
def main(league_id, shelf):

    sc = OAuth2(None, None, from_file="oauth2.json")

    gm = yfa.Game(sc, "nfl")
    lg = gm.to_league(league_id)

    print(f"It's Week {lg.current_week()}!")

    # yahoo_fantasy_api.League.matchups only returns current week's data
    if shelf:
        with shelve.open("fantasy_points") as db:
            db[str(lg.current_week())] = get_current_points(lg)

    print(get_alternative_standings(lg))


if __name__ == "__main__":
    main()
