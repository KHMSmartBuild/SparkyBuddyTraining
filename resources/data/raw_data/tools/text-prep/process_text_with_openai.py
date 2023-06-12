import os
import argparse
import openai

# Set up the API key for the OpenAI library from an environment variable or secret manager
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Define the function for generating text using the OpenAI GPT-3 API
def generate_text(prompt, 
                  model="text-davinci-003", 
                  max_tokens=2500, 
                  n=1):
    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens,
            n=n,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating text: {e}")
        return ""

# Parse the input file path as a command line argument
parser = argparse.ArgumentParser(description="Clean text in a file")
parser.add_argument("--file", type=str, help="Path to the input file")
args = parser.parse_args()

if args.file:
    input_path = args.file
else:
    input_path = "data/raw_data/Docs/langchainraw.txt"

# Load the input file
try:
    with open(input_path, "r") as f:
        input_text = f.read()
except FileNotFoundError:
    print("Input file does not exist.")
    exit()

# Generate key points from the input text
key_points_prompt = f"Extract key points from the following text: {input_text}"
key_points = generate_text(key_points_prompt)

# Generate a summary of the input text
summary_prompt = f"Summarize the following text: {input_text}"
summary = generate_text(summary_prompt)

# Extract useful information from the input text in a library format
useful_info_prompt = f"Extract useful information in a library format from the following text: {input_text}"
useful_info = generate_text(useful_info_prompt, max_tokens=800)

# Extract code snippets from the input text
code_snippet_prompt = f"Extract code snippets from the following text: {input_text}"
code_snippets = generate_text(code_snippet_prompt, max_tokens=1000)

# Create output directory if it does not exist
output_directory = "data/fine_tune_data/docs/"
os.makedirs(output_directory, exist_ok=True)

# Save outputs to files in the output directory
with open(os.path.join(output_directory, "key_points.txt"), "w") as f:
    f.write(key_points)

with open(os.path.join(output_directory, "summary.txt"), "w") as f:
    f.write(summary)

with open(os.path.join(output_directory, "useful_info.txt"), "w") as f:
    f.write(useful_info)

with open(os.path.join(output_directory, "code_snippets.txt"), "w") as f:
    f.write(code_snippets)
