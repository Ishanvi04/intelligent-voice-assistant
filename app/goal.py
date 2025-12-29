goal = {
    "name": None,
    "steps": [],
    "current_step": 0,
    "active": False
}

def start_goal(name, steps):
    goal["name"] = name
    goal["steps"] = steps
    goal["current_step"] = 0
    goal["active"] = True

