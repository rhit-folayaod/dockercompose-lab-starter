CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_code VARCHAR(10) NOT NULL UNIQUE,
    team_name VARCHAR(100) NOT NULL
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(100) NOT NULL,
    team_id INTEGER NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);