# Swiss-system Tournament Planner

Plan a [Swiss-sytem tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament) and keep track of players and matches using [Python](https://www.python.org/) and a [PostgreSQL](https://www.postgresql.org/) database.

## About project
This project was made as a submission for a [Udacity](http://www.udacity.com) Nanodegree program.  
A [Udacity supplied Vagrant VM](https://github.com/udacity/fullstack-nanodegree-vm) was used (Ubuntu, PosgreSQL and PostgreSQL CLI preconfigured).

## Requirements
1. [Python](https://www.python.org/)
2. [PostgreSQL](https://www.postgresql.org/)

## Project Files
* tournament.sql: database schema
* tournament.py: function library for database access
* tournament_test.py: client program for testing functions in tournament.py module

## Setup
Download the project files to your system of choice and import the database schema into PostgreSQL.  
_**WARNING**: The schema will overwrite existing databases named "tournament"._

Steps using [the Vagrant VM described above](https://github.com/udacity/fullstack-nanodegree-vm):  
After running the VM open up a terminal in the project directory.  
Access the PostgreSQL database server and load the database schema: 
```
$ psql -f tournament.sql
```
To run the unit tests, quit PostgreSQL:
```
$ \q
```
then run the tournament_test python script:
```
$ python tournament_test.py
```

When you see the following results, you're ready to organize a tournament:

```
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!
```


## Database contents

**TABLE: PLAYERS**  
Contents: player ID and name.

**TABLE: MATCHES**  
Contents: match results: match ID, winner and loser ID

**VIEW: STANDINGS**  
Contents: matches played by each player sorted by amount of wins.

## Tournament functions

The function library contains the following functions for organising a tournament:

FUNCTION | INPUT | OUTPUT
--- | --- | ---
connect() | | _database connection_
deleteMatches() | | None - removes all the match records from the database
deletePlayers() | | None - removes all the player records from the database
countPlayers() | | _number of currently registered players_
registerPlayer(name) | _name (string)_ | None - adds player to the tournament database (bleached)
swissPairings() | | _List of tuples, each of which contains pair of players for next round (id1, name1, id2, name2)_
reportMatch(winner, loser) | _winner ID_, _loser ID_ | None - records the outcome of a single match
playerStandings() | | _list of players and their win records, sorted by wins_

