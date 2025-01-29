import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# --------------------------------
# 1. Define the Roles and Progression
# --------------------------------
ROLE_PROGRESSION = {
    "Peasant": {
        "next_roles": ["Watch Guard", "Hunter"],
        "xp_requirement": 20  # Starting role
    },
    "Watch Guard": {
        "next_roles": ["Mercenary", "Soldier"],
        "xp_requirement": 50
    },
    "Hunter": {
        "next_roles": ["Mercenary", "Adventurer"],
        "xp_requirement": 50
    },
    "Soldier": {
        "next_roles": ["Man-at-Arms"],
        "xp_requirement": 80
    },
    "Mercenary": {
        "next_roles": ["Man-at-Arms"],
        "xp_requirement": 80
    },
    "Adventurer": {
        "next_roles": ["Mercenary", "Man-at-Arms"],
        "xp_requirement": 80
    },
    "Man-at-Arms": {
        "next_roles": ["Knight"],
        "xp_requirement": 120
    },
    "Knight": {
        "next_roles": ["Captain", "Chieftain"],
        "xp_requirement": 160
    },
    "Captain": {
        "next_roles": ["Lord"],
        "xp_requirement": 200
    },
    "Chieftain": {
        "next_roles": ["Lord", "Bandit Leader"],
        "xp_requirement": 200
    },
    "Bandit Leader": {
        "next_roles": ["Warlord"],
        "xp_requirement": 240
    },
    "Warlord": {
        "next_roles": ["Lord"],
        "xp_requirement": 300
    },
    "Lord": {
        "next_roles": ["King"],
        "xp_requirement": 400
    },
    "King": {
        "next_roles": ["Emperor"],
        "xp_requirement": 500
    },
    "Emperor": {
        "next_roles": [],
        "xp_requirement": 1000  # Max role
    }
}

# --------------------------------
# 2. Initialize Player Stats
# --------------------------------
player = {
    "name": "Unnamed Hero",
    "role": "Peasant",
    "health": 100,
    "xp": 0,
    "gold": 0
}


# --------------------------------
# 3. Core Game Logic (Adapted for GUI)
# --------------------------------

def random_event():
    """Handle a random event with possible gains/losses."""
    events = [
        "Bandit ambush",
        "Help a stray traveler",
        "Find a hidden treasure",
        "Hunt a wild beast",
        "Assist a noble's request",
    ]
    event = random.choice(events)
    log_event(f"Random event triggered: {event}")

    if event == "Bandit ambush":
        damage = random.randint(5, 15)
        xp_gain = random.randint(5, 15)
        gold_lost = random.randint(0, 5)
        player["health"] -= damage
        player["xp"] += xp_gain
        player["gold"] = max(player["gold"] - gold_lost, 0)
        log_event(f"You fought off bandits: -{damage} HP, +{xp_gain} XP, -{gold_lost} gold.")
    elif event == "Help a stray traveler":
        xp_gain = random.randint(5, 10)
        gold_gain = random.randint(5, 15)
        player["xp"] += xp_gain
        player["gold"] += gold_gain
        log_event(f"You helped a traveler: +{xp_gain} XP, +{gold_gain} gold.")
    elif event == "Find a hidden treasure":
        gold_gain = random.randint(10, 30)
        xp_gain = random.randint(0, 5)
        player["gold"] += gold_gain
        player["xp"] += xp_gain
        log_event(f"You found a hidden treasure: +{gold_gain} gold, +{xp_gain} XP.")
    elif event == "Hunt a wild beast":
        damage = random.randint(1, 10)
        xp_gain = random.randint(10, 20)
        player["health"] -= damage
        player["xp"] += xp_gain
        log_event(f"You hunted a beast: -{damage} HP, +{xp_gain} XP.")
    elif event == "Assist a noble's request":
        xp_gain = random.randint(10, 20)
        gold_gain = random.randint(0, 10)
        player["xp"] += xp_gain
        player["gold"] += gold_gain
        log_event(f"You assisted a noble: +{xp_gain} XP, +{gold_gain} gold.")

    update_status()
    check_end_game()
    check_role_upgrade()


def check_role_upgrade():
    """Check if the player qualifies to advance to the next role."""
    current_role = player["role"]
    if current_role not in ROLE_PROGRESSION:
        return

    next_roles = ROLE_PROGRESSION[current_role]["next_roles"]
    xp_req = ROLE_PROGRESSION[current_role]["xp_requirement"]

    # If already at the top or no next roles, do nothing.
    if not next_roles:
        return

    # If the player's XP >= xp_req, they may upgrade.
    if player["xp"] >= xp_req:
        # If there's only one possible next role, auto-upgrade.
        if len(next_roles) == 1:
            player["role"] = next_roles[0]
            log_event(f"You have advanced to **{player['role']}**!")
        else:
            # Prompt the user to choose among multiple roles.
            choice = simpledialog.askstring(
                "Choose Next Role",
                f"You can advance to one of: {', '.join(next_roles)}.\n"
                "Enter your choice exactly as shown, or cancel to stay."
            )
            if choice and choice in next_roles:
                player["role"] = choice
                log_event(f"You have advanced to **{player['role']}**!")
            else:
                log_event("No valid choice made. You remain in your current role.")

        update_status()
        check_end_game()


def check_end_game():
    """Check if the game should end (death or reached Emperor)."""
    if player["health"] <= 0:
        player["health"] = 0
        update_status()
        messagebox.showinfo("Game Over", "You have died! Game Over.")
        disable_actions()
    elif player["role"] == "Emperor":
        messagebox.showinfo("Victory", "You have become Emperor! Congratulations!")
        disable_actions()


# --------------------------------
# 4. GUI Functions
# --------------------------------

def update_status():
    """Update the status labels in the GUI."""
    name_label.config(text=f"Name: {player['name']}")
    role_label.config(text=f"Role: {player['role']}")
    health_label.config(text=f"Health: {player['health']}")
    xp_label.config(text=f"XP: {player['xp']}")
    gold_label.config(text=f"Gold: {player['gold']}")


def log_event(message):
    """Append a message to the log Text widget."""
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)


def disable_actions():
    """Disable all action buttons (end of game)."""
    work_button.config(state=tk.DISABLED)
    train_button.config(state=tk.DISABLED)
    rest_button.config(state=tk.DISABLED)


# --------------------------------
# 5. Action Button Handlers
# --------------------------------

def action_work():
    """Work action: small gold, small XP."""
    gold_earned = random.randint(2, 6)
    xp_gained = random.randint(1, 3)
    player["gold"] += gold_earned
    player["xp"] += xp_gained
    log_event(f"You worked hard and earned {gold_earned} gold, gained {xp_gained} XP.")

    # 1 in 5 chance to trigger a random event
    if random.randint(1, 5) == 1:
        log_event("Something unexpected happens while working...")
        random_event()

    update_status()
    check_end_game()
    check_role_upgrade()

def action_train():
    """Train action: pay gold fee, gain moderate to high XP."""
    fee = random.randint(5, 10)
    if player["gold"] >= fee:
        xp_gained = random.randint(5, 15)
        player["gold"] -= fee
        player["xp"] += xp_gained
        log_event(f"You trained with a veteran: -{fee} gold, +{xp_gained} XP.")
    else:
        log_event("Not enough gold to pay for training.")
    update_status()
    check_end_game()
    check_role_upgrade()

def action_rest():
    """Rest action: regain some health."""
    heal_amount = random.randint(10, 20)
    old_health = player["health"]
    player["health"] = min(player["health"] + heal_amount, 100)
    actual_healed = player["health"] - old_health
    log_event(f"You rested and recovered {actual_healed} health.")
    update_status()
    check_end_game()

# --------------------------------
# 6. Main GUI Setup
# --------------------------------

def start_game():
    """Initialize the game, prompt for name, and show the main window."""
    # Ask for character name
    hero_name = simpledialog.askstring("Name", "Enter your character's name:")
    if hero_name:
        player["name"] = hero_name

    update_status()
    log_event("Welcome to Rise to Power!")
    log_event(f"Your journey begins as a humble {player['role']}...")


# Create the main window
root = tk.Tk()
root.title("Rise to Power - GUI Edition")
root.geometry("600x400")

# Top frame for player stats
stats_frame = tk.Frame(root)
stats_frame.pack(pady=5)

name_label = tk.Label(stats_frame, text="Name: ???", font=("Arial", 12, "bold"))
role_label = tk.Label(stats_frame, text="Role: Peasant", font=("Arial", 12))
health_label = tk.Label(stats_frame, text="Health: 100", font=("Arial", 12))
xp_label = tk.Label(stats_frame, text="XP: 0", font=("Arial", 12))
gold_label = tk.Label(stats_frame, text="Gold: 0", font=("Arial", 12))

name_label.grid(row=0, column=0, padx=5)
role_label.grid(row=0, column=1, padx=5)
health_label.grid(row=0, column=2, padx=5)
xp_label.grid(row=0, column=3, padx=5)
gold_label.grid(row=0, column=4, padx=5)

# Middle frame for action buttons
actions_frame = tk.Frame(root)
actions_frame.pack(pady=5)

work_button = tk.Button(actions_frame, text="Work", width=12, command=action_work)
train_button = tk.Button(actions_frame, text="Train", width=12, command=action_train)
rest_button = tk.Button(actions_frame, text="Rest", width=12, command=action_rest)

work_button.grid(row=0, column=0, padx=5)
train_button.grid(row=0, column=1, padx=5)
rest_button.grid(row=0, column=2, padx=5)

# Bottom frame for logs
log_frame = tk.Frame(root)
log_frame.pack(fill=tk.BOTH, expand=True)

log_text = tk.Text(log_frame, state=tk.DISABLED, wrap=tk.WORD)
log_text.pack(fill=tk.BOTH, expand=True)

# Start the game
root.after(100, start_game)  # Slight delay so the main window appears before dialog

root.mainloop()
