# Script name: create_embeddings.py
# location = data\raw_data\tools\create_embeddings.py
# accessable from Libraries = yes


import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")



class EmbeddingGenerator:
    def __init__(self, model_name="davinci-codex"):
        self.model_name = model_name

    def generate_embeddings(self, text):
        prompt = f"Embed this text: {text}"
        response = openai.Completion.create(
            engine=self.model_name,
            prompt=prompt,
            max_tokens=16,  # Adjust the number of tokens as needed
            n=1,
            stop=None,
            temperature=0,
        )

        return response.choices[0].text
