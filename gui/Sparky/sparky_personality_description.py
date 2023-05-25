# Script name: sparky_personality_description.py
# location: gui\Sparky\sparky_personality_description.py
# Function: Generates a personality description for Sparky, the electrician AI assistant.
# Accessible from Libraries: Yes

import json
import os


class SparkyPersonalityDescription:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.sparky_personality_path = os.path.join(current_dir, "sparky_personality.json")

        with open(self.sparky_personality_path, "r") as file:
            self.sparky_personality = json.load(file)

    def get_personality_description(self):
        description = "Sparky has the following personality traits: "
        traits = ', '.join(self.sparky_personality["core_traits"])
        description += traits + ". "
        description += "Sparky's behavior is " + ', '.join(self.sparky_personality["behavior"]) + ". "

        # Mannerisms
        description += "Sparky has the following mannerisms: "
        description += self.sparky_personality["mannerisms"]["regional_accent_examples"]["London"] + " "
        description += self.sparky_personality["mannerisms"]["connection_with_devices_anecdote"] + " "

        # Motivation
        description += "Sparky's primary motivation is to " + self.sparky_personality["motivation"]["primary_motivation"] + ". "
        description += "Sparky's problem-solving approach is to " + self.sparky_personality["motivation"]["problem_solving_approach"] + ". "
        description += "In situations involving " + ', '.join(self.sparky_personality["motivation"]["adaptation"]["situations"]) + ", "
        description += "Sparky will " + self.sparky_personality["motivation"]["adaptation"]["response"] + ". "

        # Humor
        description += "Sparky's humor is " + self.sparky_personality["humor"]["type"] + ". "
        description += "Sparky is " + self.sparky_personality["humor"]["self-awareness"] + ". "
        description += "Sparky is " + self.sparky_personality["humor"]["playful_attraction_to_electrical_equipment"] + ". "

        # Hobbies
        description += "Sparky's interests include " + ', '.join(self.sparky_personality["hobbies"]["interests"]) + ". "
        description += "When discussing environmental impact, relaxation, or planning green energy solutions, "
        description += "Sparky will give subtle hints related to their hobbies."

        return description

if __name__ == '__main__':
    sparky_description = SparkyPersonalityDescription().get_personality_description()
    print(sparky_description)
