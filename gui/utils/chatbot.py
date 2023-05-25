import openai
import os
import tkinter as tk
# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define prompt with BS7671 context
prompt = "You ask Sparky Buddy a question about electrical installations in the UK. Sparky Buddy responds with an answer that is in line with the BS7671 standard."

# Function to generate response from OpenAI's GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].text.strip()
    return message

# Example usage
question = "What is the maximum permitted earth fault loop impedance for a 20A circuit with a type C circuit breaker?"
prompt = f"You ask Sparky Buddy: '{question}'.\nSparky Buddy responds: "
prompt += "The maximum permitted earth fault loop impedance for a 20A circuit with a type C circuit breaker is 1.44 ohms, according to BS7671."

response = generate_response(prompt)
print(response)
root = tk.Tk()
(root)
root.mainloop()