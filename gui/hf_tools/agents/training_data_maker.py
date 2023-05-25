import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import json

def generate_text(prompt, model, tokenizer, num_return_sequences=1, max_length=1024):
    """
    Generates text based on a given prompt using a pre-trained GPT2 language model.

    Args:
        prompt (str): The prompt to generate text from.
        model (GPT2LMHeadModel): The pre-trained GPT2 model.
        tokenizer (GPT2Tokenizer): The GPT2 tokenizer.
        num_return_sequences (int, optional): The number of text sequences to generate. Defaults to 1.
        max_length (int, optional): The maximum length of the generated text. Defaults to 1024.

    Returns:
        str: The generated text.
    """
    prompt = prompt.strip()
    prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
    generated_sequences = []
    for i in range(0, len(prompt_tokens), max_length):
        prompt_tokens_chunk = prompt_tokens[i:i+max_length]
        prompt_tokens_tensor = torch.tensor([prompt_tokens_chunk], dtype=torch.long).to(model.device)
        output = model.generate(
            prompt_tokens_tensor,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            no_repeat_ngram_size=2,
            repetition_penalty=1.5,
            temperature=1.0,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
        generated_sequences.extend(output.tolist())
    generated_text = tokenizer.decode(generated_sequences[0], skip_special_tokens=True)
    return generated_text


def split_text(prompt, tokenizer, max_tokens=1024):
    """
    Splits a given text prompt into chunks based on a maximum number of tokens.

    Args:
        prompt (str): The prompt to split into chunks.
        tokenizer (GPT2Tokenizer): The GPT2 tokenizer.
        max_tokens (int, optional): The maximum number of tokens in each chunk. Defaults to 1024.

    Returns:
        list: A list of token chunks.
    """
    tokens = tokenizer.encode(prompt, add_special_tokens=False)
    return [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]

def main():
    # Load pre-trained model and tokenizer
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    # Read the content of the cleaned text file
    cleaned_text_path = "data/processed_data/17-cleaned.txt"
    with open(cleaned_text_path, 'r') as file:
        cleaned_text = file.read()

    # Generate responses based on the cleaned text
    prompt = "What are the key takeaways from the cleaned text about electrical installations and safety regulations? " + cleaned_text
    generated_responses = generate_text(prompt, model, tokenizer, num_return_sequences=5, max_length=1024)

    # Create a dictionary for responses
    responses_dict = {'generated_responses': generated_responses.split('\n')}

    # Write the dictionary to a JSON file
    with open('responses.json', 'w') as json_file:
        json.dump(responses_dict, json_file)

if __name__ == '__main__':
    main()
