CREATE TABLE prediction_history (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL,
    opponent_code VARCHAR(10) NOT NULL,
    predicted_points DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);