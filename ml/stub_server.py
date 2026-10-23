"""
Stand-in for the real model service.

The production version of this service loads a trained scikit-learn model.
For this lab the math does not matter at all -- what matters is that there is
a second service on the network that the api has to reach by name. So this
returns a deterministic fake prediction instead, which keeps the image small
and the build fast.

The request and response shapes match the real service exactly, so the api
cannot tell the difference.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Points Predictor (lab stub)")

# Pretend league-wide average, used as the base for every prediction.
LEAGUE_AVERAGE_POINTS = 22.5


class PredictRequest(BaseModel):
    player_id: int
    team_id: int
    opponent_team_id: int


class PredictResponse(BaseModel):
    predicted_points: float
    player_avg: float
    opponent_difficulty: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    # Deterministic so every student gets the same number for the same input.
    # Nothing here is a real model; it is arithmetic chosen to look plausible.
    player_average = LEAGUE_AVERAGE_POINTS + (request.player_id % 10)
    opponent_difficulty = LEAGUE_AVERAGE_POINTS + (request.opponent_team_id % 5)
    predicted_points = player_average - (opponent_difficulty - LEAGUE_AVERAGE_POINTS)

    return PredictResponse(
        predicted_points=round(predicted_points, 2),
        player_avg=round(player_average, 2),
        opponent_difficulty=round(opponent_difficulty, 2),
    )
