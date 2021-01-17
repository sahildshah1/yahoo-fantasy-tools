# Yahoo Fantasy Tools 

## Installation

This tool depends on [yahoo-fantasy-api 2.0.1](https://pypi.org/project/yahoo-fantasy-api/2.0.1/). Note that `yahoo-fantasy-api 2.0.1` only retrives the 
current week's fantasy data.  Data is persisted using the Python Standard Library [shelve](https://docs.python.org/3/library/shelve.html) module. 


```
pip install -r requirements.txt
pip install . 
```

This tool requires an API key from Yahoo. See instructions [here.](https://yahoo-fantasy-api.readthedocs.io/en/latest/authentication.html)


### Doubleheader Scoring 

The doubleheader system is is an alternative scoring system for fantasy 
football. See details [here.](https://www.theringer.com/nfl/2019/8/6/20755201/fantasy-football-league-settings-improvement-ideas)

After each week of games (e.g. on a Tuesday), persist the week's data and get alternative standings with: 

``` 
python doubleheader.py -league_id <League ID> --shelf
```

League IDs can be found using the API: [`yahoo_fantasy_api.game.Game.league_ids`](https://yahoo-fantasy-api.readthedocs.io/en/latest/yahoo_fantasy_api.html#yahoo_fantasy_api.game.Game.league_ids).

See an example of using `yahoo_fantasy_api.game.Game.league_ids` [here.](https://pypi.org/project/yahoo-fantasy-api/)


## Development 

PRs will trigger a Github Actions workflow. The workflow file can be found [here](https://github.com/sahildshah1/yahoo-fantasy-tools/tree/master/.github/workflows)

