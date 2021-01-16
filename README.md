# Yahoo Fantasy Tools 

## Installation

```
pip install -r requirements.txt
pip install . 
```

This tool requires an API key from Yahoo. See instructions [here.](https://yahoo-fantasy-api.readthedocs.io/en/latest/authentication.html)


### Doubleheader Scoring 

The doubleheader system is is an alternative scoring system for fantasy 
football. See details [here.](https://www.theringer.com/nfl/2019/8/6/20755201/fantasy-football-league-settings-improvement-ideas)






To get alternative standings under the doubleheader system: 

``` 
python doubleheader.py -league_id <League ID>
```

League IDs can be found using the API: [`yahoo_fantasy_api.game.Game.league_ids`](https://yahoo-fantasy-api.readthedocs.io/en/latest/yahoo_fantasy_api.html#yahoo_fantasy_api.game.Game.league_ids).

See an example of using `yahoo_fantasy_api.game.Game.league_ids` [here.](https://pypi.org/project/yahoo-fantasy-api/)