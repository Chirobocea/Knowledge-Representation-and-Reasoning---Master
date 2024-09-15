import tkinter as tk
from tkinter import messagebox
import re

def split_text(text):
    pattern = r'[,\s]+'
    split_list = re.split(pattern, text.strip())
    return [item for item in split_list if item]


def convert(input_str):
    if "y" in input_str.strip().split()[0].lower():
        return True
    elif "n" in input_str.strip().split()[0].lower():
        return False
    return None

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

def run_logic(goals_input, rules):
    try:
        goals = [split_text(goals_input)]
        results = []
        for goal in goals:
            backward_result = "YES" if backward(goal, rules) else "NO"
            forward_result = "YES" if forward(goal, rules, []) else "NO"
            results.append(f"Goal: {', '.join(goal)}\nBackward result is {backward_result}\nForward result is {forward_result}\n")
        return "\n".join(results)
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def update_rules():
    rules = [["nS", "P"], ["nP", "nW", "G"], ["nG", "nE", "F"]]
    
    if sunlight_var.get() == "Yes":
        rules.append(["S"])
    if watered_var.get() == "Yes":
        rules.append(["W"])
    if protected_var.get() == "Yes":
        rules.append(["E"])
    
    return rules

def on_toggle(button, var):
    if var.get() == "Yes":
        var.set("No")
        button.config(text="No", bg="red", fg="white")
    else:
        var.set("Yes")
        button.config(text="Yes", bg="green", fg="white")

def on_run_button_click():
    goals_input = entry.get()
    if not goals_input:
        messagebox.showerror("Input Error", "Please enter goals.")
        return
    
    rules = update_rules()
    results = run_logic(goals_input, rules)
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, results)
    output_text.config(state=tk.DISABLED)

def on_run_default_button_click():
    default_goals = [["P", "nG"], ["F"], ["G"], ["P"], ["P", "G"]]
    rules = update_rules()
    
    results = []
    for goal in default_goals:
        backward_result = "YES" if backward(goal, rules) else "NO"
        forward_result = "YES" if forward(goal, rules, []) else "NO"
        results.append(f"Goal: {', '.join(goal)}\nBackward result is {backward_result}\nForward result is {forward_result}\n")
    result_str = "\n".join(results)
    
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result_str)
    output_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Logic Solver")


tk.Label(root, text="Does the plant receive sunlight?").pack(pady=5)
sunlight_var = tk.StringVar(value="No")
sunlight_button = tk.Button(root, text="No", command=lambda: on_toggle(sunlight_button, sunlight_var), bg="red", fg="white")
sunlight_button.pack(pady=5)

tk.Label(root, text="Is the plant watered regularly?").pack(pady=5)
watered_var = tk.StringVar(value="No")
watered_button = tk.Button(root, text="No", command=lambda: on_toggle(watered_button, watered_var), bg="red", fg="white")
watered_button.pack(pady=5)

tk.Label(root, text="Is the plant protected from pests?").pack(pady=5)
protected_var = tk.StringVar(value="No")
protected_button = tk.Button(root, text="No", command=lambda: on_toggle(protected_button, protected_var), bg="red", fg="white")
protected_button.pack(pady=5)

tk.Label(root, text="Enter your goals (comma-separated):").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

run_button = tk.Button(root, text="Run Logic", command=on_run_button_click)
run_button.pack(pady=5)

default_button = tk.Button(root, text="Run Default Goals", command=on_run_default_button_click)
default_button.pack(pady=5)

output_text = tk.Text(root, height=15, width=80, wrap=tk.WORD, state=tk.DISABLED)
output_text.pack(pady=5)

root.mainloop()
