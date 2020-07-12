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

def main():
    lg = yfa.League(sc,league_id)

    lg.current_week()


    lg.matchups()

    lg.standings()


if __name__ == "__main__":
    main()


