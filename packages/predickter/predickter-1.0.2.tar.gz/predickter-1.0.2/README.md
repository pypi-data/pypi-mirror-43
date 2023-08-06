# predickter

A Python package, to get live scores, live commentary and scorecards.

<b>Instllation</b>
<code>
pip install predickter
</code>

<b>Features</b>

* Get information upcoming, live and recently concluded matches
  * series name
  * match status
  * venue
  * toss
  * match official
  * squads
* Get mini scorecards for live matches
  * Batsman currently batting along with their scores,runs,fours,sixes etc.
  * Bowlers currently bowling along with their wickets,overs,maidens etc.
  * Summary of all the innings
  * Last three overs events
  * Current patnership and run rate
* Commentary for live matches
* Scorecard for live and past matches

<b>Basic Usage</b>

Import the pycricbuzz library.

```python
from predickter import Predickter
p = Predickter()
```

<b>Get all the matches(live,upcoming and recently finished matches)</b>
```python
print p.matches()
```

Each match will have an attribute 'id'. Use this 'id' to get matchinfo, scorecard, brief score and commentary of matches.

<b>Get information about a match</b>

```
print p.matchinfo(match['id'])
```

<b>Get brief score of a match</b>

```python
print p.livescore(match['id'])
```

<b>Get scorecard of a match</b>

```python
print p.scorecard(match['id'])
```

