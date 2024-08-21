import random

from utils import prompt_user, load_json, DataPath


def trigger_random_events(player_data, events):
    """Trigger a random event based on probability and age range."""
    for event in events:
        if event['age_range'][0] <= player_data['age'] <= event['age_range'][1]:
            if random.random() < event['probability']:
                print(f"Random Event: {event['description']}")
                for key, value in event['impact'].items():
                    player_data[key] += value
                break

    return player_data


def early_life_phase(player_data):
    """Handles decisions and events in the Early Life phase (Ages 16-22)."""
    print("Early Life Phase")

    if player_data['age'] == 18:
        # Educational decision at age 18
        prompt = "Choose your educational path:"
        options = load_json(DataPath.EDUCATION)
        choice = prompt_user(prompt, options)

        # TODO:
        """ 
            1. Add opportunities for college to vary in price (scholarships, tuition assistance, etc.)
            2. Add specific trade school routes that also vary in price (electrician, plumber, welder, etc.)
        """

        match choice:

            case "High School":
                """Start working immediately"""
                occupations = load_json(DataPath.OCCUPATIONS)
                occupation = prompt_user("Choose your career path:", occupations[0]["occupations"])
                player_data['occupation'] = occupation
                player_data['income'] = occupation["Income"]["Starting"]

            case _:
                player_data['skills']['education'] = choice["id"]
                player_data['bank'] -= choice["Cost"]

    # TODO: Example decision - part-time job income during education
    # if player_data['age'] < 23 and player_data['skills']['education'] in ["Trade School", "College"]:
    #     player_data['bank'] += 1000
    #     player_data['happiness'] -= 5  # Slight happiness decrease due to work

    print(f'Age: {player_data["age"]}, Bank: ${player_data["bank"]}, Happiness: {player_data["happiness"]}')

    return player_data


def young_adult_phase(player_data):
    """Handles decisions and events in the Young Adult phase (Ages 23-30)."""
    print("Young Adult Phase")

    if player_data["age"] == 23:
        # Career decision at age 23
        prompt = "Choose your career path:"
        occupations = load_json(DataPath.OCCUPATIONS)

        match player_data['skills']['education']:
            case "High School":
                choice = prompt_user(prompt, occupations[0]["occupations"])

            case "Trade School":
                choice = prompt_user(prompt, occupations[1]["occupations"])
                
            case "University/College":
                choice = prompt_user(prompt, occupations[2]["occupations"])

            case "Bootcamp":
                choice = prompt_user(prompt, occupations[3]["occupations"])
            
        player_data['occupation'] = choice["id"]
        player_data['bank'] += choice["Income"]["Starting"]
        player_data['income'] = choice["Income"]["Starting"]

    print(f"Age: {player_data['age']}, "
          f"Bank: ${player_data['bank']}, "
          f"Happiness: {player_data['happiness']}")

    return player_data


def mid_life_phase(player_data):
    """Handles decisions and events in the Mid-Life phase (Ages 31-50)."""
    print("Mid-Life Phase")

    if player_data['age'] == 35:
        """Investment decision at age 35"""

        investments = load_json(DataPath.INVESTMENT)
        choice = prompt_user("Investment Opportunity: ", investments)
        choice["current_value"] = choice["initial_value"]

        player_data["assets"].append(choice)

    print(f"Age: {player_data['age']}, "
          f"Bank: ${player_data['bank']}")

    return player_data


# You can add more phases here following the same structure:
# def mid_life_phase(player_data):
# def pre_retirement_phase(player_data):
# def retirement_phase(player_data):
