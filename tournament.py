#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import bleach


def connect(db='tournament'):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        DB = psycopg2.connect("dbname=%s" % db)
        cursor = DB.cursor()
        return DB, cursor
    except:
        raise IOError('Error connecting to database %s' % db)


def deleteMatches():
    """Remove all the match records from the database."""
    DB, cursor = connect()
    cursor.execute("DELETE FROM matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, cursor = connect()
    cursor.execute("DELETE FROM players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB, cursor = connect()
    cursor.execute("SELECT COUNT(*) FROM players;")
    num_players = cursor.fetchone()[0]
    DB.close()
    return num_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, cursor = connect()
    name_bleached = bleach.clean(name, strip=True)
    cursor.execute("INSERT INTO players (player_name) VALUES (%s);",
              (name_bleached,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, cursor = connect()
    cursor.execute("SELECT * FROM standings;")
    player_standings = cursor.fetchall()
    DB.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, cursor = connect()
    cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s);",
              (winner, loser,))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB, cursor = connect()
    cursor.execute("SELECT * FROM standings;")
    wins_list = cursor.fetchall()
    DB.close()

    match_pairs = []
    standings_count = len(wins_list)

    for x in range(0, standings_count - 1, 2):
        match_pair = (wins_list[x][0], wins_list[x][1], wins_list[x + 1][0],
                      wins_list[x + 1][1])
        match_pairs.append(match_pair)

    return match_pairs
