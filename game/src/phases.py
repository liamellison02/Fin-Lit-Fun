import random
import json

def load_events():
    """Load random events from the events.json file."""
    with open("../data/events.json", "r") as file:
        events = json.load(file)
    return events

def trigger_random_event(player_data, events):
    """Trigger a random event based on probability and age range."""
    for event in events:
        if player_data['age'] >= event['age_range'][0] and player_data['age'] <= event['age_range'][1]:
            if random.random() < event['probability']:
                print(f"Random Event: {event['description']}")
                for key, value in event['impact'].items():
                    player_data[key] += value
                break
    return player_data

def early_life_phase(player_data):
    """Handles decisions and events in the Early Life phase (Ages 16-22)."""
    print("Early Life Phase")
    player_data['age'] += 1

    if player_data['age'] == 18:
        # Educational decision at age 18
        print("Choose your educational path:")
        print("1. High School Only (Immediate work)")
        print("2. Trade School (2 years)")
        print("3. College (4 years)")
        print("4. Bootcamp (1 year)")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            player_data['skills']['education'] = "High School"
            player_data['financial_status'] += 5000  # Start working immediately
        elif choice == "2":
            player_data['skills']['education'] = "Trade School"
            player_data['financial_status'] -= 2000  # Cost of trade school
        elif choice == "3":
            player_data['skills']['education'] = "College"
            player_data['financial_status'] -= 10000  # Cost of college
        elif choice == "4":
            player_data['skills']['education'] = "Bootcamp"
            player_data['financial_status'] -= 5000  # Cost of bootcamp

    # Example decision: part-time job income during education
    if player_data['age'] < 23 and player_data['skills']['education'] in ["Trade School", "College"]:
        player_data['financial_status'] += 1000
        player_data['happiness'] -= 5  # Slight happiness decrease due to work

    print(f"Age: {player_data['age']}, Financial Status: ${player_data['financial_status']}, Happiness: {player_data['happiness']}")
    return player_data


def young_adult_phase(player_data):
    """Handles decisions and events in the Young Adult phase (Ages 23-30)."""
    print("Young Adult Phase")
    player_data['age'] += 1

    if player_data['age'] == 24:
        # Career decision at age 24
        if player_data['skills']['education'] == "High School":
            print("Choose your career path:")
            print("1. Retail Worker")
            print("2. Factory Worker")
            choice = input("Enter the number of your choice: ")

            if choice == "1":
                player_data['financial_status'] += 20000
                player_data['happiness'] += 5
            elif choice == "2":
                player_data['financial_status'] += 25000
                player_data['happiness'] -= 10

        elif player_data['skills']['education'] == "Trade School":
            print("Choose your career path:")
            print("1. Technician")
            print("2. Skilled Trade Worker")
            choice = input("Enter the number of your choice: ")

            if choice == "1":
                player_data['financial_status'] += 30000
                player_data['happiness'] += 10
            elif choice == "2":
                player_data['financial_status'] += 35000
                player_data['happiness'] -= 5

        elif player_data['skills']['education'] == "College":
            print("Choose your career path:")
            print("1. Junior Developer")
            print("2. Accountant")
            choice = input("Enter the number of your choice: ")

            if choice == "1":
                player_data['financial_status'] += 50000
                player_data['happiness'] += 10
            elif choice == "2":
                player_data['financial_status'] += 55000
                player_data['happiness'] += 5

        elif player_data['skills']['education'] == "Bootcamp":
            print("Choose your career path:")
            print("1. Software Engineer")
            print("2. IT Support Specialist")
            choice = input("Enter the number of your choice: ")

            if choice == "1":
                player_data['financial_status'] += 60000
                player_data['happiness'] += 15
            elif choice == "2":
                player_data['financial_status'] += 40000
                player_data['happiness'] += 10

    print(f"Age: {player_data['age']}, Financial Status: ${player_data['financial_status']}, Happiness: {player_data['happiness']}")
    return player_data

def mid_life_phase(player_data):
    """Handles decisions and events in the Mid-Life phase (Ages 31-50)."""
    print("Mid-Life Phase")
    player_data['age'] += 1

    if player_data['age'] == 35:
        print("Investment Opportunity:")
        print("1. Buy Stocks (High risk, high return)")
        print("2. Invest in Real Estate (Moderate risk, steady return)")
        print("3. Start a Retirement Plan (Low risk, secure return)")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            player_data['financial_status'] -= 10000  # Investment cost
            player_data['financial_status'] += random.randint(5000, 20000)  # Variable return
        elif choice == "2":
            player_data['financial_status'] -= 20000
            player_data['financial_status'] += random.randint(15000, 25000)
        elif choice == "3":
            player_data['financial_status'] -= 5000
            player_data['financial_status'] += 7000

    print(f"Age: {player_data['age']}, Financial Status: ${player_data['financial_status']}")
    return player_data


# You can add more phases here following the same structure:
# def mid_life_phase(player_data):
# def pre_retirement_phase(player_data):
# def retirement_phase(player_data):
