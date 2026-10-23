import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(__file__))

from main import app
import main as main_module

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # Frontend HTML should be returned, not JSON
    assert "text/html" in response.headers["content-type"]
    assert "NBA Player Predictor" in response.text


def test_sample_prediction():
    response = client.get("/sample-prediction")
    assert response.status_code == 200

    data = response.json()
    assert "player" in data
    assert "opponent" in data
    assert "predicted_points" in data


def test_read_teams():
    original_function = main_module.get_all_teams

    def fake_get_all_teams():
        return [
            {"id": 1, "team_code": "MIN", "team_name": "Minnesota Timberwolves"},
            {"id": 2, "team_code": "BOS", "team_name": "Boston Celtics"}
        ]

    main_module.get_all_teams = fake_get_all_teams

    response = client.get("/teams")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["team_code"] == "MIN"

    main_module.get_all_teams = original_function


def test_read_players():
    original_function = main_module.get_all_players

    def fake_get_all_players():
        return [
            {
                "id": 1,
                "player_name": "Anthony Edwards",
                "team_id": 1,
                "team_code": "MIN",
                "team_name": "Minnesota Timberwolves"
            }
        ]

    main_module.get_all_players = fake_get_all_players

    response = client.get("/players")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["player_name"] == "Anthony Edwards"

    main_module.get_all_players = original_function


def test_create_player():
    original_add_player = main_module.add_player

    def fake_add_player(player_name, team_id):
        return 99

    main_module.add_player = fake_add_player

    response = client.post(
        "/players",
        json={
            "player_name": "Jalen Brunson",
            "team_id": 1
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Player added successfully"
    assert data["player_id"] == 99

    main_module.add_player = original_add_player


def test_create_sample_prediction():
    original_get_player_by_id = main_module.get_player_by_id
    original_save_prediction = main_module.save_prediction

    def fake_get_player_by_id(player_id):
        return {
            "id": player_id,
            "player_name": "Anthony Edwards",
            "team_id": 1,
            "team_code": "MIN",
            "team_name": "Minnesota Timberwolves"
        }

    def fake_save_prediction(player_id, opponent_code, predicted_points):
        return {
            "id": 10,
            "created_at": "2026-04-22 12:00:00"
        }

    main_module.get_player_by_id = fake_get_player_by_id
    main_module.save_prediction = fake_save_prediction

    response = client.post(
        "/predictions/sample",
        json={
            "player_id": 1,
            "opponent_code": "BOS"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Sample prediction created successfully"
    assert data["prediction"]["player_name"] == "Anthony Edwards"
    assert data["prediction"]["opponent_code"] == "BOS"

    main_module.get_player_by_id = original_get_player_by_id
    main_module.save_prediction = original_save_prediction


def test_read_prediction_history():
    original_function = main_module.get_prediction_history

    def fake_get_prediction_history():
        return [
            {
                "id": 1,
                "player_name": "Anthony Edwards",
                "opponent_code": "BOS",
                "predicted_points": 26.0,
                "created_at": "2026-04-22 12:00:00"
            }
        ]

    main_module.get_prediction_history = fake_get_prediction_history

    response = client.get("/predictions")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["player_name"] == "Anthony Edwards"

    main_module.get_prediction_history = original_function