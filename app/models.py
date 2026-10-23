from pydantic import BaseModel


class PlayerCreate(BaseModel):
    player_name: str
    team_id: int


class SamplePredictionRequest(BaseModel):
    player_id: int
    opponent_code: str