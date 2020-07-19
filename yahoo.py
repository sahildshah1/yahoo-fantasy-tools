#!/usr/bin/env python

"""
Each week you will have to track which teams finished in the top half 
of the league in scoring, and you’ll need to maintain a set of alternate 
standings all season.

"""

from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa


def _get_yahoo_api_session():
    return OAuth2(None, None, from_file='keys.json')


def get_top_half_teams():
    """ foo

    Parameters
    ----------
    foo: str
        Platform ID of the credential

    Returns
    list of tuple of str
        foo 

    """

def get_alternative_standings():
    """ foo

    Parameters
    ----------
    foo: str
        Platform ID of the credential

    Returns
    list of tuple of str
        foo 

    """

def get_current_points(lg):
    """ Get current points

    Parameters
    ----------
    lg : yahoo_fantasy_api.League
        An instance of the yahoo_fantasy_api League object
        
    Returns
    ---------
    dict {str: str}
        {team key: points}

    """

    matchups_content = lg.matchups()

    matchups = matchups_content['fantasy_content']['league'][1]['scoreboard']['0']['matchups']

    foo = {}

    for matchup in range(matchups['count']):

        teams = matchups[str(matchup)]['matchup']['0']['teams']

        for team in range(teams['count']):

            team_key = teams[str(team)]['team'][0][0]['team_key']
            team_points = teams[str(team)]['team'][1]['team_points']['total']

            foo[team_key] = team_points

    return foo


def main():

    sc = _get_yahoo_api_session()

    gm = yfa.Game(sc, 'nfl')
    gm.league_ids(2018)
    lg = gm.to_league('380.l.765649')

    lg.current_week()

    get_current_points(lg)

    lg.standings()


if __name__ == "__main__":
    main()


