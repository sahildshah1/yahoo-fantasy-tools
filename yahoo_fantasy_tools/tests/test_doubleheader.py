"""
Tests for doubleheader
"""

import unittest.mock as mock

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


DOUBLEHEADER_BOUNUS = {

    "380.l.765649.t.1": 0,
    "380.l.765649.t.3": 0,
    "380.l.765649.t.4": 0,
    "380.l.765649.t.10": 1,
    "380.l.765649.t.5": 1,
    "380.l.765649.t.8": 0,
    "380.l.765649.t.6": 1,
    "380.l.765649.t.7": 1,

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
@mock.patch("yahoo_fantasy_tools.doubleheader.get_top_half_teams")
def test_get_alternative_standings(m_top_half_teams, m_get_current_standings):

    m_get_current_standings.return_value = OUTCOMES
    m_top_half_teams.return_value = TOP_HALF_TEAMS

    m_lg = mock.Mock()
    m_lg.teams.return_value = TEAMS

    actual = doubleheader.get_alternative_standings(m_lg)

    expected = pd.DataFrame(
        {
            "team_key": [
                "380.l.765649.t.10",
                "380.l.765649.t.4",
                "380.l.765649.t.7",
                "380.l.765649.t.6",
                "380.l.765649.t.5",
                "380.l.765649.t.8",
                "380.l.765649.t.1",
                "380.l.765649.t.3",
                "380.l.765649.t.9",
                "380.l.765649.t.2",
            ],
            "team_name": [
                "Easy Drake oven",
                "The Gurley Show",
                "Comeback Train",
                "Shady",
                "BetterGoEatSome Soup",
                "Sy's Slam-Dunk Team",
                "...brown do for you",
                "Yolo swag 420 dab",
                "Elementary Watson!",
                "Goal #1 Draft Pick",
            ],
            "doubleheader_wins": [11, 7, 8, 13, 8, 6, 7, 6, 4, 4],
            "doubleheader_losses": [4, 8, 7, 2, 7, 9, 8, 9, 11, 11],
            "wins": [10, 7, 7, 12, 7, 6, 7, 6, 4, 4],
            "losses": [4, 7, 7, 2, 7, 8, 7, 8, 10, 10],
            "ties": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "percentage": [
                0.714,
                0.5,
                0.5,
                0.857,
                0.5,
                0.429,
                0.5,
                0.429,
                0.286,
                0.286,
            ],
            "doubleheader_percentage": [
                0.7333333333333333,
                0.4666666666666667,
                0.5333333333333333,
                0.8666666666666667,
                0.5333333333333333,
                0.4,
                0.4666666666666667,
                0.4,
                0.26666666666666666,
                0.26666666666666666,
            ],
        }
    )

    pd.testing.assert_frame_equal(expected, actual)


def test_get_current_standings():
    """Ensure get_current_standings returns correct answer
    """

    m_lg = mock.Mock()

    m_lg.standings.return_value = STANDINGS

    actual = doubleheader.get_current_standings(m_lg)

    expected = OUTCOMES

    assert expected == actual


def test_get_doubleheader_bonus():
    """Ensure get_doubleheader_bonus returns correct answer
    """

    m_lg = mock.Mock()



    actual = doubleheader.get_doubleheader_bonus(m_lg)

    expected = 

    assert expected = actual 





@mock.patch("yahoo_fantasy_tools.doubleheader.get_current_points")
def test_get_top_half_teams(m_get_current_points):

    m_get_current_points.return_value = POINTS

    m_lg = mock.Mock()

    actual = doubleheader.get_top_half_teams(m_lg)

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
