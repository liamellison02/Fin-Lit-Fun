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
    player_data['age'] += 1

    if player_data['age'] == 18:
        # Educational decision at age 18
        print("Choose your educational path:")
        print("1. High School Only (Immediate work)")
        print("2. Trade School (2 years)")
        print("3. College (4 years)")
        print("4. Bootcamp (1 year)")
        choice = input("Enter the number of your choice: ")

        # TODO:
        """ 
            1. Add opportunities for college to vary in price (scholarships, tuition assistance, etc.)
            2. Add specific trade school routes that also vary in price (electrician, plumber, welder, etc.)
        """
        match choice:

            case "1":
                """Start working immediately"""
                player_data['skills']['education'] = "High School"
                player_data['financial_status'] += 5000

            case "2":
                """Trade school route; 2 years; Cost: $2000"""
                player_data['skills']['education'] = "Trade School"
                player_data['financial_status'] -= 2000  # Cost of trade school

            case "3":
                """College route; 4 years; Cost: $40000"""
                player_data['skills']['education'] = "College"
                player_data['financial_status'] -= 40000  # Cost of college

            case "4":
                """Bootcamp route; 1 year; Cost: $10000"""
                player_data['skills']['education'] = "Bootcamp"
                player_data['financial_status'] -= 10000  # Cost of bootcamp

    # TODO: Example decision - part-time job income during education
    # if player_data['age'] < 23 and player_data['skills']['education'] in ["Trade School", "College"]:
    #     player_data['financial_status'] += 1000
    #     player_data['happiness'] -= 5  # Slight happiness decrease due to work

    print(f"Age: {player_data['age']}, "
          f"Financial Status: ${player_data['financial_status']}, "
          f"Happiness: {player_data['happiness']}")

    return player_data


def young_adult_phase(player_data):
    """Handles decisions and events in the Young Adult phase (Ages 23-30)."""
    print("Young Adult Phase")
    player_data['age'] += 1

    if player_data['age'] == 24:
        # Career decision at age 24
        match player_data['skills']['education']:

            case "High School":
                print("Choose your career path:")
                print("1. Retail Worker")
                print("2. Factory Worker")
                choice = input("Enter the number of your choice: ")
                while choice != "1" and choice != "2":  # Input validation
                    choice = input("Enter the number of your choice (1 or 2): ")
                if choice == "1":
                    player_data['financial_status'] += 20000
                    player_data['happiness'] += 5
                elif choice == "2":
                    player_data['financial_status'] += 25000
                    player_data['happiness'] -= 10

            case "Trade School":
                print("Choose your career path:")
                print("1. Technician")
                print("2. Skilled Trade Worker")
                choice = input("Enter the number of your choice: ")
                while choice != "1" and choice != "2":  # Input validation
                    choice = input("Enter the number of your choice (1 or 2): ")
                if choice == "1":
                    player_data['financial_status'] += 30000
                    player_data['happiness'] += 10
                elif choice == "2":
                    player_data['financial_status'] += 35000
                    player_data['happiness'] -= 5

            case "College":
                print("Choose your career path:")
                print("1. Junior Developer")
                print("2. Accountant")
                choice = input("Enter the number of your choice: ")

                while choice != "1" and choice != "2":  # Input validation
                    choice = input("Enter the number of your choice (1 or 2): ")

                if choice == "1":
                    player_data['financial_status'] += 50000
                    player_data['happiness'] += 10
                elif choice == "2":
                    player_data['financial_status'] += 55000
                    player_data['happiness'] += 5

            case "Bootcamp":
                print("Choose your career path:")
                print("1. Software Engineer")
                print("2. IT Support Specialist")
                choice = input("Enter the number of your choice: ")

                while choice != "1" and choice != "2":  # Input validation
                    choice = input("Enter the number of your choice (1 or 2): ")

                if choice == "1":
                    player_data['financial_status'] += 60000
                    player_data['happiness'] += 15
                elif choice == "2":
                    player_data['financial_status'] += 40000
                    player_data['happiness'] += 10

    print(f"Age: {player_data['age']}, "
          f"Financial Status: ${player_data['financial_status']}, "
          f"Happiness: {player_data['happiness']}")

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

        while choice != "1" and choice != "2" and choice != "3":
            choice = input("Enter the number of your choice (1, 2, or 3): ")

        match choice:
            case "1":
                player_data['financial_status'] -= 10000  # Investment cost
                player_data['financial_status'] += random.randint(5000, 20000)  # Variable return
            case "2":
                player_data['financial_status'] -= 20000
                player_data['financial_status'] += random.randint(15000, 25000)
            case "3":
                player_data['financial_status'] -= 5000
                player_data['financial_status'] += 7000

    print(f"Age: {player_data['age']}, "
          f"Financial Status: ${player_data['financial_status']}")

    return player_data


# You can add more phases here following the same structure:
# def mid_life_phase(player_data):
# def pre_retirement_phase(player_data):
# def retirement_phase(player_data):
