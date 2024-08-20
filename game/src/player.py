import json
import os
import uuid

# Path to the player data JSON file
DATA_PATH = "../data/player.json"

def load_player():
    """Load the player profile from a JSON file."""
    try:
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r") as file:
                return json.load(file)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to load player data: {e}")
    return None

def save_player(player_data):
    """Save the player profile to a JSON file."""
    with open(DATA_PATH, "w") as file:
        json.dump(player_data, file, indent=4)

def create_player(name):
    """Create a new player profile."""
    player_data = {
        "player_id": str(uuid.uuid4()),  # Generate a unique ID for the player
        "name": name,
        "age": 16,
        "health": 100,
        "happiness": 100,
        "financial_status": 0,
        "skills": {
            "education": "High School",
            "work_experience": 0
        },
        "education_level": "None",
        "game_progress": {}
    }
    save_player(player_data)
    return player_data
