-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- My own notes and work below:
-- I will use this style guide http://www.sqlstyle.guide/, which was the first 
-- googe results for "SQL Style Guide"
-- https://docs.c9.io/docs/setting-up-postgresql

\c postgres

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament


DROP TABLE IF EXISTS players;

DROP TABLE IF EXISTS matches;

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    winner TEXT,
    loser TEXT
);

GRANT ALL PRIVILEGES ON TABLE matches TO ubuntu;
GRANT ALL PRIVILEGES ON TABLE players TO ubuntu;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to ubuntu;

-- The following VIEWS; win_counts, match_counts, players_wins_counts, and 
-- players_standings are all created to fulfill the needs of the 
-- playerStandings() function.
-- I had trouble including more than two columns in an aggregations select.
-- When I'm ready, I'll return to this: 
-- https://www.udacity.com/course/viewer#!/c-ud197-nd/l-3490418600/e-3576048992/m-3475179083

    
-- Create a view with at least one row for each player, and one row for
-- each of their wins.

CREATE VIEW win_counts AS 
    SELECT name, COUNT(winner) AS wins                                        
        FROM (
            -- Left join players with all their winning matches
            SELECT players.id, players.name, matches.winner
            FROM players LEFT JOIN matches 
            ON players.name = matches.winner
            ) AS players_wins
        GROUP BY name
        ORDER BY wins DESC;
    

CREATE VIEW match_counts AS
    SELECT name, COUNT(winner) AS matches_played
    FROM (
        -- LEFT join players with all their matches played
        SELECT players.id, players.name, matches.winner, matches.loser
        FROM players LEFT JOIN matches
        ON ( players.name = matches.winner OR players.name = matches.loser)
        ) AS players_matches
    GROUP BY name
    ORDER BY matches_played DESC;

CREATE VIEW players_win_counts AS
    SELECT players.id, players.name, win_counts.wins
        FROM players LEFT JOIN win_counts
        ON players.name = win_counts.name;

CREATE VIEW players_standings AS
    SELECT players_win_counts.id, players_win_counts.name, players_win_counts.wins, match_counts.matches_played
        FROM players_win_counts LEFT JOIN match_counts
        ON players_win_counts.name = match_counts.name
        ORDER BY players_win_counts.wins DESC;


GRANT ALL PRIVILEGES ON players_standings TO ubuntu;
