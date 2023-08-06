# predickter

A Python package, to get live scores, live commentary and scorecards.

<b>Instllation</b>
<code>
pip install predickter
</code>

<b>Basic Usage</b>

Import the predickter library.

```python
from predickter import Precrickter
p = Predickter()
```

<b>Get all the matches(live,upcoming and recently finished matches)</b>
```python
print (p.matches())
```

Each match will have an attribute 'id'. Use this 'id' to get matchinfo, scorecard, brief score and commentary of matches.

<b>Get information about a match</b>

```
print (p.matchinfo(match['id']))
```

<b>Get brief score of a match</b>

```python
print (p.livescore(match['id']))
```

<b>Get scorecard of a match</b>

```python
print (p.scorecard(match['id']))
```
<b>Get live commentary </b>
```
print (p.commentary(match['id']))
```



