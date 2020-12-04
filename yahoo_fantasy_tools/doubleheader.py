"""
Compute  "doubleheader" standings for the current week of the season
"""

from collections import Counter
from sys import exit
import statistics

import pandas as pd
import click
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa


def get_alternative_standings(lg, current_week):
    """ Compute "doubleheader" standings

    Parameters
    ----------
    lg : yahoo_fantasy_api.League
        An instance of the yahoo_fantasy_api League class
    current_week : int
        Current week of the season

    Returns
    --------
    pandas.DataFrame

    """

    standings = get_current_standings(lg)

    # Add win if in top half of league and loss if in bottom half
    top_half_counts = Counter()
    for week in range(1, current_week + 1):
        top_half_counts.update(get_top_half_teams(lg, week))

    tms = lg.teams()

    df = pd.DataFrame(
        {
            "team_name": [tms[key]["name"] for key in standings.keys()],
            "doubleheader_wins": [
                int(val["wins"]) + top_half_counts.get(key, 0)
                for key, val in standings.items()
            ],
            "points_for": [val["points_for"] for val in standings.values()],
            "doubleheader_losses": [
                int(val["losses"]) + (current_week - top_half_counts.get(key, 0))
                for key, val in standings.items()
            ],
            "wins": [int(val["wins"]) for val in standings.values()],
            "losses": [int(val["losses"]) for val in standings.values()],
            "ties": [int(val["ties"]) for val in standings.values()],
            "percentage": [float(val["percentage"]) for val in standings.values()],
        }
    )

    df["doubleheader_percentage"] = df["doubleheader_wins"] / (
        df["doubleheader_wins"] + df["doubleheader_losses"]
    )

    return df.sort_values(by=["doubleheader_wins", "points_for"], ascending=False)


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

    s = lg.standings()

    standings = {}
    for team in s:
        standings[team["team_key"]] = team["outcome_totals"]
        standings[team["team_key"]]["points_for"] = float(team["points_for"])

    return standings


def get_top_half_teams(lg, week):
    """ Get top half teams

    Parameters
    ----------
    lg : yahoo_fantasy_api.League
        An instance of the yahoo_fantasy_api League class
    week : int
        Week number

    Returns
    -------
    set 

    """

    points = get_points_for_week(lg, week)

    median_points = statistics.median(
        [float(points) for points in list(points.values())]
    )

    return {team for team, points in points.items() if float(points) > median_points}


def get_points_for_week(lg, week=None):
    """ Get points for a given week

    Parameters
    ----------
    lg : yahoo_fantasy_api.League
        An instance of the yahoo_fantasy_api League object
    week : int
        Week number

    Returns
    ---------
    dict

    """

    matchups_content = lg.matchups(week)

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

    return get_points_for_week(lg)


@click.command()
@click.option("--league-id", help="League ID")
@click.option("--year", help="Year to look for")
def main(league_id, year):

    sc = OAuth2(None, None, from_file="oauth2.json")

    gm = yfa.Game(sc, "nfl")
    ids = gm.league_ids(year=year)

    for l_id in ids:
        if league_id in l_id:
            league_id = l_id
            break
    else:
        print("No league found with that ID and year!")
        exit(1)

    lg = gm.to_league(league_id)
    week = lg.current_week()

    print(f"The current week is {week}")

    print(get_alternative_standings(lg, week))


if __name__ == "__main__":
    main()
