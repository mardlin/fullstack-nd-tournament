-- Table definitions for the tournament project.
--
-- Following http://www.sqlstyle.guide/

\c postgres

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament


DROP TABLE IF EXISTS players;

DROP TABLE IF EXISTS matches;

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    winner INT REFERENCES players (id) ON DELETE CASCADE,
    loser INT REFERENCES players (id) ON DELETE CASCADE,
    CHECK (winner <> loser)
);

-- The following VIEWS; win_counts, match_counts, players_wins_counts, and 
-- players_standings are all created to fulfill the needs of the 
-- playerStandings() function.
    
-- Create a view with at least one row for each player, and one row for
-- each of their wins.

-- View1: Returns the count of a player's wins
CREATE VIEW win_counts AS 
    SELECT id, COUNT(winner) AS wins                                        
        FROM (
            -- Left join players with all their winning matches
            SELECT players.id, players.name, matches.winner
            FROM players LEFT JOIN matches 
            ON players.id = matches.winner
            ) AS players_wins
        GROUP BY id
        ORDER BY wins DESC;
    
-- View2: Returns the count of a player's matches
CREATE VIEW match_counts AS
    SELECT id, COUNT(winner) AS matches_played
    FROM (
        -- LEFT join players with all their matches played
        SELECT players.id, players.name, matches.winner, matches.loser
        FROM players LEFT JOIN matches
        ON ( players.id = matches.winner OR players.id = matches.loser)
        ) AS players_matches
    GROUP BY id
    ORDER BY matches_played DESC;

-- View3: Joins the players wins (View1) to the players table
CREATE VIEW players_win_counts AS
    SELECT players.id, players.name, win_counts.wins
        FROM players LEFT JOIN win_counts
        ON players.id = win_counts.id;

-- View4: Joins View2 and View3
-- This will give a table with columns: (id, name, wins, matches_played)
CREATE VIEW players_standings AS
    SELECT players_win_counts.id, players_win_counts.name, 
        players_win_counts.wins, match_counts.matches_played
        FROM players_win_counts LEFT JOIN match_counts
        ON players_win_counts.id = match_counts.id
        ORDER BY players_win_counts.wins DESC;
        
        
-- Create a view listing all players who have not had a BYE (ie. a match where the 
-- loser is NULL)
CREATE VIEW players_w_byes AS
    SELECT players.id              
    FROM players, matches
    WHERE players.id = winner AND matches.loser IS NULL;    
        


