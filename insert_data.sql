DELETE FROM players;
DELETE FROM matches;

INSERT INTO players (name) values ('John');
INSERT INTO players (name) values ('Kunal');
INSERT INTO players (name) values ('Dawn');
INSERT INTO players (name) values ('Mitch');
INSERT INTO players (name) values ('Cole');
INSERT INTO players (name) values ('Clara');

INSERT INTO matches (winner, loser) values ('John','Cole');
INSERT INTO matches (winner, loser) values ('Dawn','Cole');
INSERT INTO matches (winner, loser) values ('John','Mitch');
INSERT INTO matches (winner, loser) values ('Dawn','Mitch');
INSERT INTO matches (winner, loser) values ('Cole', 'Kunal');
INSERT INTO matches (winner, loser) values ('Kunal','Dawn');
INSERT INTO matches (winner, loser) values ('Cole','Harris');
-- Clara has no matches
-- INSERT INTO matches (winner, loser) values ('Clara','Dawn');