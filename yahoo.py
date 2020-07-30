#!/usr/bin/env python

"""
Each week you will have to track which teams finished in the top half 
of the league in scoring, and you’ll need to maintain a set of alternate 
standings all season.

"""

import statistics 

import pandas as pd 
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa


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



def get_top_half_teams(points):
    """ foo

    Parameters
    ----------
    foo: str
        Platform ID of the credential

    Returns
    list of tuple of str
        foo

    """

    m = statistics.median([float(i) for i in list(points.values())])

    return {key for key,value in points.items() if float(value) > m}



def get_alternative_standings(standings, top_half_teams):
    """ foo

    Parameters
    ----------
    foo: str
        Platform ID of the credential

    Returns
    list of tuple of str
        foo 

    """

    df = pd.DataFrame({'team_key': list(standings.keys()),
                       'wins': [int(val['wins']) for val in standings.values()],
                       'losses': [int(val['losses']) for val in standings.values()],
                       'ties': [int(val['ties']) for val in standings.values()],
                       'percentage': [float(val['percentage']) for val in standings.values()],
                       'doubleheader_wins': [int(val['wins']) + 1 if key in top_half_teams
                                              else int(val['wins'])
                                              for key, val in standings.items()],
                        'doubleheader_losses': [int(val['losses']) + 1 if key  not in top_half_teams
                                              else int(val['losses'])
                                              for key, val in standings.items()]})

    df['doubleheader_percentage'] = df['doubleheader_wins']/ (df['doubleheader_wins'] + df['doubleheader_losses'])


    df order by adjusted percentage 



def get_current_standings(lg):
    """ Get current standingss

    Parameters
    ----------
    lg : yahoo_fantasy_api.League
        An instance of the yahoo_fantasy_api League object
        
    Returns
    ---------

    """

    standings_content = lg.standings()

    return {bar['team_key']: bar['outcome_totals'] for bar in standings_content}



def main():

    sc = OAuth2(None, None, from_file='keys.json')

    gm = yfa.Game(sc, 'nfl')
    gm.league_ids(2018)
    lg = gm.to_league('380.l.765649')

    lg.current_week()

    get_current_points(lg)



if __name__ == "__main__":
    main()


