import json

with open("sparky_script.json") as f:
    data = json.load(f)

core_traits = data["core_traits"]
behavior = data["behavior"]
mannerisms = data["mannerisms"]
motivation = data["motivation"]
humor = data["humor"]
hobbies = data["hobbies"]

def create_llm(core_traits, behavior, mannerisms, motivation, humor, hobbies):
    """Creates a large language model with the specified characteristics.

    Args:
        core_traits: A list of core traits that the LLM should have.
        behavior: A list of behaviors that the LLM should exhibit.
        mannerisms: A dictionary of mannerisms that the LLM should have.
        motivation: A dictionary of motivations that the LLM should have.
        humor: A dictionary of humor that the LLM should have.
        hobbies: A list of hobbies that the LLM should have.

    Returns:
        A large language model with the specified characteristics.
    """

    llm = Bard()

    for trait in core_traits:
        llm.add_trait(trait)

    for behavior in behavior:
        llm.add_behavior(behavior)

    for mannerism in mannerisms:
        llm.add_mannerism(mannerism)

    for motivation in motivation:
        llm.add_motivation(motivation)

    for humor in humor:
        llm.add_humor(humor)

    for hobby in hobbies:
        llm.add_hobby(hobby)

    return llm


llm = create_llm(core_traits, behavior, mannerisms, motivation, humor, hobbies)

print(llm)
