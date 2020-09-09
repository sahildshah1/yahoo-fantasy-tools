"""
Compute  "doubleheader" standings for the current week of the season
"""

import statistics

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

    # Add win if in top half of league and loss if in bottom half
    top_half_teams = get_top_half_teams(lg)

    tms = lg.teams()

    df = pd.DataFrame(
        {
            "team_key": list(standings.keys()),
            "team_name": [tms[key]["name"] for key in standings.keys()],
            "doubleheader_wins": [
                int(val["wins"]) + 1 if key in top_half_teams else int(val["wins"])
                for key, val in standings.items()
            ],
            "doubleheader_losses": [
                int(val["losses"]) + 1
                if key not in top_half_teams
                else int(val["losses"])
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


def get_top_half_teams(lg):
    """ Get top half teams

    Parameters
    ----------
    lg : yahoo_fantasy_api.League
        An instance of the yahoo_fantasy_api League class

    Returns
    -------
    set 

    """

    points = get_current_points(lg)

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
def main(league_id):

    sc = OAuth2(None, None, from_file="oauth2.json")

    gm = yfa.Game(sc, "nfl")
    lg = gm.to_league(league_id)

    print(f"The current week is {lg.current_week()}")

    print(get_alternative_standings(lg))


if __name__ == "__main__":
    main()
