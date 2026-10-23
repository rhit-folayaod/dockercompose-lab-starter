import logging
import os
import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
import httpx

from db import (
    check_database,
    get_all_teams,
    get_all_players,
    get_player_by_id,
    add_player,
    save_prediction,
    get_prediction_history,
)
from models import PlayerCreate, SamplePredictionRequest
from logging_config import configure_logging, get_logger, request_id_var

# Configure logging once at startup
configure_logging(level=logging.INFO)
logger = get_logger("nba.api")

app = FastAPI()


# ---------------------------------------------------------------------------
# Middleware: assign a request ID and log every request/response
# ---------------------------------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)

    start = time.time()
    logger.info(f"--> {request.method} {request.url.path}")

    try:
        response = await call_next(request)
    except Exception:
        # An unhandled exception is a severe outage — log at CRITICAL
        logger.critical(
            f"Unhandled error during {request.method} {request.url.path}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "request_id": request_id},
        )

    duration_ms = round((time.time() - start) * 1000, 1)
    logger.info(
        f"<-- {request.method} {request.url.path} "
        f"status={response.status_code} duration={duration_ms}ms"
    )
    # Return the request id to the client so they can reference it in bug reports
    response.headers["X-Request-ID"] = request_id
    return response


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def read_root():
    logger.debug("Serving frontend index.html")
    static_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    return FileResponse(static_path)


@app.get("/health")
def health_check():
    try:
        database_ok = check_database()

        if database_ok:
            logger.debug("Health check passed: database is up")
            return {"status": "ok", "api": "up", "database": "up"}

        logger.critical("Health check: database reported DOWN — service degraded")
        return {"status": "error", "api": "up", "database": "down"}
    except Exception as error:
        logger.error(f"Health check raised an exception: {error}")
        return {
            "status": "error",
            "api": "up",
            "database": "down",
            "message": str(error),
        }


@app.get("/teams")
def read_teams():
    teams = get_all_teams()
    logger.info(f"Returned {len(teams)} teams")
    return teams


@app.get("/players")
def read_players():
    players = get_all_players()
    logger.info(f"Returned {len(players)} players")
    return players


@app.get("/players/{player_id}")
def read_player(player_id: int):
    logger.debug(f"Looking up player_id={player_id}")
    player = get_player_by_id(player_id)

    if player is None:
        logger.warning(f"Player not found: player_id={player_id}")
        raise HTTPException(status_code=404, detail="Player not found")

    return player


@app.post("/players")
def create_player(player: PlayerCreate):
    try:
        new_id = add_player(player.player_name, player.team_id)
        logger.info(f"Created player '{player.player_name}' with id={new_id}")
        return {"message": "Player added successfully", "player_id": new_id}
    except Exception as error:
        logger.error(f"Failed to create player '{player.player_name}': {error}")
        raise HTTPException(status_code=500, detail="Could not create player")


@app.get("/sample-prediction")
def sample_prediction():
    logger.debug("Returning static sample prediction")
    return {
        "player": "Shai Gilgeous-Alexander",
        "opponent": "LAL",
        "predicted_points": 30.4,
    }


@app.post("/predictions/sample")
def create_sample_prediction(request: SamplePredictionRequest):
    player = get_player_by_id(request.player_id)

    if player is None:
        logger.warning(f"Sample prediction: player not found id={request.player_id}")
        raise HTTPException(status_code=404, detail="Player not found")

    predicted_points = 25.0 + request.player_id

    try:
        saved_prediction = save_prediction(
            request.player_id, request.opponent_code, predicted_points
        )
    except Exception as error:
        logger.error(f"Failed to save sample prediction: {error}")
        raise HTTPException(status_code=500, detail="Could not save prediction")

    logger.info(
        f"Sample prediction saved id={saved_prediction['id']} "
        f"player_id={request.player_id} points={predicted_points}"
    )
    return {
        "message": "Sample prediction created successfully",
        "prediction": {
            "id": saved_prediction["id"],
            "player_name": player["player_name"],
            "opponent_code": request.opponent_code,
            "predicted_points": predicted_points,
            "created_at": saved_prediction["created_at"],
        },
    }


@app.post("/predictions/ml")
def create_ml_prediction(request: SamplePredictionRequest):
    logger.info(
        f"ML prediction requested: player_id={request.player_id} "
        f"opponent={request.opponent_code}"
    )

    player = get_player_by_id(request.player_id)
    if player is None:
        logger.warning(f"ML prediction: player not found id={request.player_id}")
        raise HTTPException(status_code=404, detail="Player not found")

    # Find the opponent team's numeric ID from its code
    opponent_team_id = 1  # fallback
    for team in get_all_teams():
        if team["team_code"] == request.opponent_code:
            opponent_team_id = team["id"]
            break
    else:
        logger.warning(
            f"ML prediction: opponent code '{request.opponent_code}' not found, "
            f"using fallback team id {opponent_team_id}"
        )

    ml_url = os.environ.get("ML_SERVICE_URL", "http://nba-ml:80") + "/predict"
    payload = {
        "player_id": request.player_id,
        "team_id": player["team_id"],
        "opponent_team_id": opponent_team_id,
    }
    logger.debug(f"Calling ML service at {ml_url} with payload={payload}")

    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.post(ml_url, json=payload)
            response.raise_for_status()
            ml_result = response.json()
            predicted_points = ml_result["predicted_points"]
    except Exception as e:
        logger.error(f"ML service call failed: {e}")
        raise HTTPException(status_code=503, detail=f"ML service unavailable: {e}")

    logger.info(
        f"ML service returned predicted_points={predicted_points} "
        f"for player_id={request.player_id}"
    )

    try:
        saved = save_prediction(
            request.player_id, request.opponent_code, predicted_points
        )
    except Exception as error:
        logger.error(f"Failed to save ML prediction: {error}")
        raise HTTPException(status_code=500, detail="Could not save prediction")

    logger.info(f"ML prediction saved id={saved['id']}")
    return {
        "message": "ML prediction created successfully",
        "prediction": {
            "id": saved["id"],
            "player_name": player["player_name"],
            "opponent_code": request.opponent_code,
            "predicted_points": predicted_points,
            "player_avg": ml_result.get("player_avg"),
            "opponent_difficulty": ml_result.get("opponent_difficulty"),
            "created_at": saved["created_at"],
            "source": "ML model",
        },
    }


@app.get("/predictions")
def read_prediction_history():
    history = get_prediction_history()
    logger.info(f"Returned {len(history)} prediction history records")
    return history