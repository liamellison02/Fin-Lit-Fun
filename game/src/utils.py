# TODO - set output to UI instead of console
def prompt_user(prompt: str, decisions: dict, input_message: str = "Enter the number of your choice: "):
    """Given a prompt and available options (decisions), returns user's decision."""
    print(prompt)  # outputs to a popup menu
    print('\n')

    valid_inputs = set()
    i = 1

    for k1, v1 in decisions:
        # outputs decision name to a popup menu
        print(f'{i}. {k1}')  

        # outputs decision attributes to the overview panel
        for k2, v2 in v1:
            print(f'{k2}: {v2}')  
            
        valid_inputs.add(str(i))
        i += 1

    choice = input(input_message)
    while choice not in valid_inputs:
        print(f"Invalid input: {choice}; Please enter a valid number.")
        choice = input(input_message)
    
    choice = int(choice) - 1
    return decisions[choice]
