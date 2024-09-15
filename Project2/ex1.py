def convert(input_str):
    if "y" in input_str.strip().split()[0].lower():
        return True
    elif "n" in input_str.strip().split()[0].lower():
        return False
    return None


def get_input(prompt):
    while True:
        i = input(prompt)
        b = convert(i)
        if b is not None:
            return b
        print("Invalid input. Please enter 'y' or 'n'.")


def proces(clause):
    positive_literal = None
    negated_literals = []
    for literal in clause:
        if literal.startswith("n"):
            negated_literals.append(literal[1:]) 
        else:
            positive_literal = literal

    return positive_literal, negated_literals


def check_solved_literals(literals, solved_literals):
    return all(literal in solved_literals for literal in literals)


def backward(goals, rules):
    if not goals:
        return True
    
    goal = goals[0]
    rest_goals = goals[1:]


    if goal.startswith("n"):
        positive_goal = goal[1:]
        result = backward([positive_goal], rules)
        if not result:
            return backward(rest_goals, rules)
        return False

    for clause in rules:
        positive_literal, negated_literals = proces(clause)

        if goal == positive_literal:
            new_goals = negated_literals + rest_goals
            if backward(new_goals, rules):
                return True

    return False


def forward(goals, rules, solved_literals):
    while True:
        progress = False
        for clause in rules:
            positive_literal, negated_literals = proces(clause)
            if check_solved_literals(negated_literals, solved_literals) and positive_literal not in solved_literals:
                solved_literals.append(positive_literal)
                progress = True

        if not progress:
            break


    for goal in goals:
        if goal.startswith("n"):
            if goal[1:] in solved_literals: 
                return False
        else:
            if goal not in solved_literals:
                return False

    return True


"""
Rules:
If a plant receives sunlight, then it can perform photosynthesis.
If a plant performs photosynthesis and it is watered regularly, then the plant will grow.
If a plant grows and is protected from pests, then the plant will produce flowers.
Questions:
Does the plant receive sunlight? (yes/no)
Is the plant watered regularly? (yes/no)
Is the plant protected from pests? (yes/no)
"""


while True:

    rules = [["nS", "P"], ["nP", "nW", "G"], ["nG", "nE", "F"]]

    if get_input("Does the plant receive sunlight? [y/n]\n"):
        rules.append(["S"]) 
    if get_input("Is the plant watered regularly? [y/n]\n"):
        rules.append(["W"]) 
    if get_input("Is the plant protected from pests? [y/n]\n"):
        rules.append(["E"]) 

    goals = [["P", "nG"], ["F"], ["G"], ["P"]]  

    print("    Results:\n")
    for goal in goals:
        print(f"Goal: {', '.join(goal)}")
        print("Backward result is", "YES" if backward(goal, rules) else "NO")
        print("Forward result is", "YES" if forward(goal, rules, []) else "NO")

    print("\n")
    if "stop" in input("To terminate the loop enter 'stop' else press enter\n").strip().lower():
        break
