"""
Tests for doubleheader
"""

import unittest.mock as mock
from collections import Counter

import pandas as pd

import yahoo_fantasy_tools.doubleheader as doubleheader
from const import MATCHUPS, STANDINGS, TEAMS

POINTS = {
    "380.l.765649.t.1": "100.12",
    "380.l.765649.t.3": "98.30",
    "380.l.765649.t.4": "118.34",
    "380.l.765649.t.10": "144.66",
    "380.l.765649.t.5": "133.28",
    "380.l.765649.t.8": "105.52",
    "380.l.765649.t.6": "118.84",
    "380.l.765649.t.7": "141.02",
}

TOP_HALF_TEAMS = {
    "380.l.765649.t.10",
    "380.l.765649.t.5",
    "380.l.765649.t.6",
    "380.l.765649.t.7",
}


OUTCOMES = {
    "380.l.765649.t.10": {"wins": "10", "losses": "4", "ties": 0, "percentage": ".714"},
    "380.l.765649.t.4": {"wins": "7", "losses": "7", "ties": 0, "percentage": ".500"},
    "380.l.765649.t.7": {"wins": "7", "losses": "7", "ties": 0, "percentage": ".500"},
    "380.l.765649.t.6": {"wins": "12", "losses": "2", "ties": 0, "percentage": ".857"},
    "380.l.765649.t.5": {"wins": "7", "losses": "7", "ties": 0, "percentage": ".500"},
    "380.l.765649.t.8": {"wins": "6", "losses": "8", "ties": 0, "percentage": ".429"},
    "380.l.765649.t.1": {"wins": "7", "losses": "7", "ties": 0, "percentage": ".500"},
    "380.l.765649.t.3": {"wins": "6", "losses": "8", "ties": 0, "percentage": ".429"},
    "380.l.765649.t.9": {"wins": "4", "losses": "10", "ties": 0, "percentage": ".286"},
    "380.l.765649.t.2": {"wins": "4", "losses": "10", "ties": 0, "percentage": ".286"},
}


@mock.patch("yahoo_fantasy_tools.doubleheader.get_current_standings")
@mock.patch("yahoo_fantasy_tools.doubleheader.get_bonus_wins")
def test_get_alternative_standings(m_get_bonus_wins, m_get_current_standings):

    m_get_current_standings.return_value = OUTCOMES
    m_get_bonus_wins.return_value = Counter({'380.l.765649.t.6': 2,
                                             '380.l.765649.t.5': 2,
                                             '380.l.765649.t.7': 2,
                                             '380.l.765649.t.10': 2})

    m_lg = mock.Mock()
    m_lg.teams.return_value = TEAMS

    actual = doubleheader.get_alternative_standings(m_lg)

    expected = pd.DataFrame({'team_key': ['380.l.765649.t.6',
  '380.l.765649.t.10',
  '380.l.765649.t.7',
  '380.l.765649.t.5',
  '380.l.765649.t.4',
  '380.l.765649.t.1',
  '380.l.765649.t.8',
  '380.l.765649.t.3',
  '380.l.765649.t.9',
  '380.l.765649.t.2'],
 'team_name': ['Shady',
  'Easy Drake oven',
  'Comeback Train',
  'BetterGoEatSome Soup',
  'The Gurley Show',
  '...brown do for you',
  "Sy's Slam-Dunk Team",
  'Yolo swag 420 dab',
  'Elementary Watson!',
  'Goal #1 Draft Pick'],
 'wins': [12, 10, 7, 7, 7, 7, 6, 6, 4, 4],
 'bonus_wins': [2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
 'total_wins': [14, 12, 9, 9, 7, 7, 6, 6, 4, 4],
 'ties': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    pd.testing.assert_frame_equal(expected, actual)


def test_get_current_standings():
    """Ensure get_current_standings returns correct answer
    """

    m_lg = mock.Mock()

    m_lg.standings.return_value = STANDINGS

    actual = doubleheader.get_current_standings(m_lg)

    expected = OUTCOMES

    assert expected == actual


@mock.patch("yahoo_fantasy_tools.doubleheader.shelve.open")
def test_get_bonus_wins(m_open):

    db = {"15": POINTS, "16": POINTS}

    m_open.return_value.__enter__.return_value = db

    actual = doubleheader.get_bonus_wins()

    expected = Counter({'380.l.765649.t.6': 2,
                        '380.l.765649.t.5': 2,
                        '380.l.765649.t.7': 2,
                        '380.l.765649.t.10': 2})

    assert expected == actual 


def test_get_top_half_teams():

    actual = doubleheader.get_top_half_teams(POINTS)

    expected = TOP_HALF_TEAMS

    assert expected == actual


def test_get_current_points():
    """Ensure get_current_points returns correct answer
    """
    m_lg = mock.Mock()

    m_lg.matchups.return_value = MATCHUPS

    actual = doubleheader.get_current_points(m_lg)

    expected = POINTS

    assert expected == actual
