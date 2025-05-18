import random

from controllers import FILE

from pathlib import Path
import pandas as pd

# Get the base directory dynamically
BASE_DIR = Path(__file__).resolve().parent.parent

# Construct file paths dynamically
election_stats_path = BASE_DIR / "data/election_stats.json"
election_results_path = BASE_DIR / "data/election_results.csv"
current_election_path = BASE_DIR / "output/mayor_data.json"

# Load data using the dynamically generated paths
election_stats = FILE.get_json(election_stats_path)
election_results = pd.read_csv(election_results_path)
current_election = FILE.get_json(current_election_path)

# Ensure 'mayor' column exists before accessing
if "mayor" not in election_results.columns:
    raise KeyError(f"'mayor' column not found in {election_results_path}")

class Mayor:
    def __init__(self, name):
        self.name = name
        self.perks = []


def generate_perk_prediction(active_candidates):
    res = {candidate: [] for candidate in active_candidates}

    for dy, mayor in enumerate(election_results["mayor"]):
        if dy == 0 or mayor not in active_candidates:
            continue

        max_perks = len(election_stats[mayor]["perks_map"])

        # If this is the first time the mayor is elected, assign one random perk
        if not res[mayor]:
            available_perks = list(range(1, max_perks + 1))
            initial_perk = random.choice(available_perks)
            res[mayor].append(initial_perk)

            # For each subsequent election cycle, determine perk gain
            for i in range(dy):
                other_candidates = election_results["other_candidates"][i]
                if mayor in other_candidates:
                    new_perk_chance = election_stats[mayor]["new_perk_chance"] / 100  # Convert percentage to decimal

                    # Attempt to gain a new perk based on new_perk_chance
                    if random.random() < new_perk_chance:
                        available_perks = list(set(range(1, max_perks + 1)) - set(res[mayor]))
                        if available_perks:
                            new_perk = random.choice(available_perks)
                            res[mayor].append(new_perk)



    return res

