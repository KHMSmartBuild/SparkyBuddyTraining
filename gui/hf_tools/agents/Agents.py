import openai
import os

# Replace with your OpenAI API key
openai.api_key = "your-api-key"

# Define your agents and their roles
agents = {
    "task_master": {"name": "Task Master", "role": "management"},
    "why_agent": {"name": "Why Agent", "role": "supervisor"},
    "safety_agent": {"name": "Safety Agent", "role": "supervisor"},
    "understanding_agent": {"name": "Understanding Agent", "role": "worker"},
    "worker_agent": {"name": "Worker Agent", "role": "worker"},
}


def generate_response(prompt):
    """
    Generates a response using OpenAI GPT-3 engine.

    Args:
        prompt (str): The prompt to be sent to the GPT-3 engine.

    Returns:
        str: The generated response text.
    """
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def main():
    """
    Main function that runs the Sparky Buddy 3 agent interaction loop.
    """
    print("Welcome to the Sparky Buddy 3 Agent!")
    print("Type 'quit' to exit the program.\n")
    while True:
        user_prompt = input("Enter your prompt: ").strip()
        if user_prompt.lower() == "quit":
            break
        # Send the user prompt to the Understanding Agent
        understanding_prompt = f"{agents['understanding_agent']['name']} receives a user input: {user_prompt}. How does it process the input and delegate tasks to other agents?"
        understanding_response = generate_response(understanding_prompt)
        # Delegate tasks based on the Understanding Agent's response
        task_master_prompt = f"{agents['task_master']['name']} receives instructions from the Understanding Agent: {understanding_response}. How does it coordinate with other agents to complete the task?"
        task_master_response = generate_response(task_master_prompt)
        # Collect results from the worker agents
        worker_prompt = f"{agents['worker_agent']['name']} receives instructions from the Task Master: {task_master_response}. How does it execute the task and provide results?"
        worker_response = generate_response(worker_prompt)
        # Review the results with the Why Agent and Safety Agent
        why_agent_prompt = f"{agents['why_agent']['name']} reviews the results from the Worker Agent: {worker_response}. How does it analyze the results?"
        why_agent_response = generate_response(why_agent_prompt)
        safety_agent_prompt = f"{agents['safety_agent']['name']} reviews the results from the Worker Agent: {worker_response}. How does it ensure safety and compliance?"
        safety_agent_response = generate_response(safety_agent_prompt)
        # Combine the responses from different agents
        final_response = f"Results: {worker_response}\nWhy Agent Analysis: {why_agent_response}\nSafety Agent Compliance: {safety_agent_response}"
        print(f"Agent: {final_response}\n")

if __name__ == "__main__":
    main()