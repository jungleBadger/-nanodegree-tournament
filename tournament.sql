-- Table definitions for the tournament project.

-- Create database (drop it if it exists) and connect
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\connect tournament


-- Create the database tables
CREATE TABLE players(
    player_id serial PRIMARY KEY,
    player_name text
);

CREATE TABLE matches(
    match_id serial PRIMARY KEY,
    winner integer REFERENCES players(player_id),
    loser integer REFERENCES players(player_id)
);


-- Create view for standings (matches played by each player sorted by number of wins)
CREATE VIEW standings AS
    SELECT players.player_id as player_id, players.player_name,
    (SELECT count(*) FROM matches WHERE matches.winner = players.player_id) as matches_won,
    (SELECT count(*) FROM matches WHERE players.player_id in (winner, loser)) as matches_played
    FROM players
    GROUP BY players.player_id
    ORDER BY matches_won DESC;
