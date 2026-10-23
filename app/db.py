import os
import psycopg2


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "nba_predictor"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )


def check_database():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT 1;")
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0] == 1


def get_all_teams():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, team_code, team_name
        FROM teams
        ORDER BY team_name;
    """)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    teams = []
    for row in rows:
        teams.append({
            "id": row[0],
            "team_code": row[1],
            "team_name": row[2]
        })

    return teams


def get_all_players():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT p.id, p.player_name, p.team_id, t.team_code, t.team_name
        FROM players p
        JOIN teams t ON p.team_id = t.id
        ORDER BY p.player_name;
    """)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    players = []
    for row in rows:
        players.append({
            "id": row[0],
            "player_name": row[1],
            "team_id": row[2],
            "team_code": row[3],
            "team_name": row[4]
        })

    return players


def get_player_by_id(player_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT p.id, p.player_name, p.team_id, t.team_code, t.team_name
        FROM players p
        JOIN teams t ON p.team_id = t.id
        WHERE p.id = %s;
    """, (player_id,))
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "player_name": row[1],
        "team_id": row[2],
        "team_code": row[3],
        "team_name": row[4]
    }


def add_player(player_name, team_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO players (player_name, team_id)
        VALUES (%s, %s)
        RETURNING id;
    """, (player_name, team_id))

    new_id = cursor.fetchone()[0]
    connection.commit()

    cursor.close()
    connection.close()

    return new_id


def save_prediction(player_id, opponent_code, predicted_points):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO prediction_history (player_id, opponent_code, predicted_points)
        VALUES (%s, %s, %s)
        RETURNING id, created_at;
    """, (player_id, opponent_code, predicted_points))

    row = cursor.fetchone()
    connection.commit()

    cursor.close()
    connection.close()

    return {
        "id": row[0],
        "created_at": str(row[1])
    }


def get_prediction_history():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ph.id, p.player_name, ph.opponent_code, ph.predicted_points, ph.created_at
        FROM prediction_history ph
        JOIN players p ON ph.player_id = p.id
        ORDER BY ph.created_at DESC;
    """)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "player_name": row[1],
            "opponent_code": row[2],
            "predicted_points": float(row[3]),
            "created_at": str(row[4])
        })

    return history