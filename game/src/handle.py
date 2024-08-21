import random

from player import save_player
from phases import trigger_random_events, early_life_phase, young_adult_phase, mid_life_phase


def handle_turn(player, events, occupations):
    """Handles the logic for each turn (year) in the game."""
    player["age"] += 1

    
    # TODO - Fix this putrid code
    i = 0
    while i < 4:
        if player["skills"]["education"] == occupations[i]["id"]:
            possible_occupations = occupations[i]["occupations"]
            i = 0
            while i < len(possible_occupations):
                if possible_occupations[i]["id"] == player["occupation"]:
                    player["income"] += player["income"] * possible_occupations[i]["Income"]["Increase_Rate"]
                    break
                i += 1
            break
        i += 1
    player["bank"] += player["income"]

    for asset in player["assets"]:
        asset["current_value"] += asset["current_value"] * (asset["rate"] + (asset["volatility"] * random.uniform(-1.0, 1.0)))

    player = trigger_random_events(player, events)
    
    if player["age"] < 23:
        player = early_life_phase(player)
    elif player["age"] < 31:
        player = young_adult_phase(player)
    else:
        player = mid_life_phase(player)
    
    save_player(player)
    
    return player