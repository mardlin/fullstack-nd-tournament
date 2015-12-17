#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# Example:
# conn = connect()
# c = conn.cursor()
# c.execute("your query;")
# conn.commit() 
# conn.close()


import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # create the DB connection
    DB = connect()
    # create the cursor
    cursor = DB.cursor()
    # Define and execture the SQL command string
    command = " DELETE FROM matches; "
    cursor.execute(command)
    # Commit the change
    DB.commit()
    # close the connection
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    command = "DELETE FROM players;"
    cursor.execute(command)
    DB.commit()
    DB.close()
    

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    command = "SELECT COUNT(*) FROM players"
    cursor.execute(command)
    # fetchall returns [(0L,)], and fetchone returns (0L,), so use fetchone()[0]
    results = cursor.fetchone()[0]
    DB.close()
    return results


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    command = "INSERT INTO players (name) VALUES (%s)"
    # Using the proper psycopg2 string replacement format for sanitization
    cursor.execute( command, (name,) )
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    
    # All the SQL magic is in tournament.sql
    command = "select * from players_standings;"
    
    cursor.execute(command)
    results = cursor.fetchall()
    DB.close()
    return results



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()
    command = "INSERT INTO matches (winner, loser) values (%s, %s);"
    cursor.execute(command, (winner, loser,))
    DB.commit()
    DB.close()
    
 
 
# def swissPairings():
#     """Returns a list of pairs of players for the next round of a match.
  
#     Assuming that there are an even number of players registered, each player
#     appears exactly once in the pairings.  Each player is paired with another
#     player with an equal or nearly-equal win record, that is, a player adjacent
#     to him or her in the standings.
  
#     Returns:
#       A list of tuples, each of which contains (id1, name1, id2, name2)
#         id1: the first player's unique id
#         name1: the first player's name
#         id2: the second player's unique id
#         name2: the second player's name
#     """


