import uuid
import json

from utils import load_json, DataPath


def save_player(player_data):
    """Save the player profile to a JSON file."""
    path = str(DataPath.PLAYER.value)
    with open(path, "w") as file:
        json.dump(player_data, file, indent=4)


def create_player(name):
    """Create a new player profile."""
    assets = load_json(DataPath.ASSETS)
    debit_card = assets[0]
    debit_card["current_value"] = debit_card["initial_value"]

    player_data = {
        "player_id": str(uuid.uuid4()),  # Generate a unique ID for the player
        "name": name,
        "age": 16,
        "health": 90,
        "happiness": 50,
        "bank": 200,
        "income": 0,
        "skills": {
            "education": "High School",
            "work_experience": 0
        },
        "education_level": "None",
        "occupation": "None",
        "assets": [debit_card],
        "liabilities": [],
        "status_effects": [],
        "game_progress": {}
    }

    save_player(player_data)
    return player_data
