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


def connect(database_name = "tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:    
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except: 
        print ("Connection error")


def deleteMatches():
    """Remove all the match records from the database."""
    # create the DB connection and cursor
    db, cursor = connect()
    # Define and execute the SQL command string
    command = " DELETE FROM matches; "
    cursor.execute(command)
    # Commit the change
    db.commit()
    # close the connection
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    command = "DELETE FROM players;"
    cursor.execute(command)
    db.commit()
    db.close()
    

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    command = "SELECT COUNT(*) FROM players"
    cursor.execute(command)
    # fetchall returns [(0L,)], and fetchone returns (0L,), so use fetchone()[0]
    results = cursor.fetchone()[0]
    db.close()
    return results


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    command = "INSERT INTO players (name) VALUES (%s)"
    # Using the proper psycopg2 string replacement format for sanitization
    cursor.execute( command, (name,) )
    db.commit()
    db.close()


def playerStandings(limit=None, offset=None):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    
    Optionally, this function can be used to select a subset of the standings
    based on the limit and offset arguments.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, cursor = connect()
    
    # The players_standing view is created in tournament.sql
    # The following lines build out the rest of the query according to the 
    # arguments provided.
    command = "SELECT * FROM players_standings LIMIT %s OFFSET %s;"
    cursor.execute(command, (limit, offset,))
    results = cursor.fetchall()
    db.close()
    return results



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    command = "INSERT INTO matches (winner, loser) values (%s, %s);"
    cursor.execute(command, (winner, loser,))
    db.commit()
    db.close()

# Here I define a new function for use in swissPairings()
def playerHasBye(player):
    """Checks whether a player has have already been given a BYE.
    
    Args: 
        player: the id number of a player
        
    Returns:
        boolean
    """
    db, cursor = connect()
    command = "SELECT * FROM players_w_byes WHERE id = %s;"
    cursor.execute( command, ( player,) )
    result = cursor.fetchone() is not None
    db.close()
    return result
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    
    If there is an odd number of players, a BYE will be given to the top ranked 
    player who does not yet have a BYE. 
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
      In the case of a BYE, a tuple will contain (id1, name1, null, null)
        
    """
    
    count = countPlayers()
    standings = playerStandings()
    print standings
    matches = []
    
    # For the case of an odd number of players
    if count % 2 != 0: 
        # find the top ranked player without a BYE            
        for (i,n,w,m) in standings: 
            # check if this player has a BYE
            if playerHasBye( i ):
                # if they don't have a BYE, give them one!
                matches.append( (i , n, None, None) )
                # delete this entry from standings
                standings.remove( (i,n,w,m) )
                break
    
    print standings
    index = 1
    # Work through the standings two at a time to build the tuples.
    for (i, n, w, m) in standings:
        # start a new tuple when i is odd
        if ( index % 2 == 1):
            player1 = ()
            player1 += (i, n,)
            print index, player1
        # add to the tuple when i is even, then append to the list
        if ( index % 2 == 0):
            player2 = ()
            player2 += (i, n,)
            matches.append(player1 + player2)    
            print index, player2
        index += 1
    return matches
    
            
        
        
    


