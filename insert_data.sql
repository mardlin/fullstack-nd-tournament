DELETE FROM players;
DELETE FROM matches;

INSERT INTO players (name) VALUES ('John');
INSERT INTO players (name) VALUES ('Kunal');
INSERT INTO players (name) VALUES ('Dawn');
INSERT INTO players (name) VALUES ('Mitch');
INSERT INTO players (name) VALUES ('Cole');
INSERT INTO players (name) VALUES ('Clara');

INSERT INTO matches (winner, loser) VALUES ('1','5');
INSERT INTO matches (winner, loser) VALUES ('3','5');
INSERT INTO matches (winner, loser) VALUES ('1','4');
INSERT INTO matches (winner, loser) VALUES ('3','4');
INSERT INTO matches (winner, loser) VALUES ('5', '2');
INSERT INTO matches (winner, loser) VALUES ('2','3');
INSERT INTO matches (winner, loser) VALUES ('5','7');
-- Clara has no matches
-- INSERT INTO matches (winner, loser) VALUES ('Clara','Dawn');