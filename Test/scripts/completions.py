import os
import openai

# Set the API key
openai.api_key = os.environ.get("OPENAI_API_KEY") or "YOUR_API_KEY"

# Define the prompt
prompt_text = 'The quick brown fox jumps over the lazy dog.'

# Generate completions
def generate_completions(prompt, max_tokens=5):
    """
    Generates completions for the given prompt using OpenAI API.
    :param prompt: The input text to generate completions for.
    :param max_tokens: The maximum number of tokens to generate.
    :return: A list of generated completions.
    """
    try:
        completions = openai.Completion.create(engine='davinci-codex', prompt=prompt, max_tokens=max_tokens, n=1)
        return completions.choices
    except Exception as e:
        print(f'Error: {e}')
        return []

if __name__ == '__main__':
    completions = generate_completions(prompt_text, max_tokens=5)
    for completion in completions:
        print(completion.text)
