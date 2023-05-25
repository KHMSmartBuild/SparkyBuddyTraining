import spacy
from spacy.util import minibatch, compounding
from spacy.pipeline.textcat import DEFAULT_SINGLE_TEXTCAT_MODEL
from pathlib import Path
import random
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization_id = os.getenv("OPENAI_ORGANIZATION_ID")

import logging

logging.basicConfig(filename='ChatGPT_convo_sorter.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def generate_response(prompt):
    if not openai.api_key or not openai.organization_id:
        logging.warning("Invalid OpenAI API key or organization ID")
        return ""

    response = openai.ChatCompletion.create(
        engine="gpt4",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.3,
    )

    message = response.choices[0].text.strip()
    return message


def get_additional_categories(text):
    prompt = f"Based on the text provided, suggest additional categories:\n{text}"
    response = generate_response(prompt)
    categories = [cat.strip() for cat in response.split(',') if cat.strip()]
    return categories

def generate_example_sentences(category, num_examples=5):
    prompt = f"Generate {num_examples} example sentences about {category}:"
    response = generate_response(prompt)
    sentences = response.split("\n")
    return sentences[:num_examples]

# Define your categories
categories = ["products", "projects", "companies", "plans"]

# Generate example sentences for each category
example_sentences = {}
for category in categories:
    example_sentences[category] = generate_example_sentences(category)

# Prepare the training data
train_data = []
for category, sentences in example_sentences.items():
    for sentence in sentences:
        cats = {cat: 1 if cat == category else 0 for cat in categories}
        train_data.append((sentence, {"cats": cats}))

# Read the content of the file
with open("gui/Sparky/paste_conversion_here.txt", "r") as file:
    text = file.read()

additional_categories = get_additional_categories(text)

# Get categories from GPT
main_categories = ["products", "projects", "companies", "plans", "other"]
categories = list(set(main_categories + additional_categories))


config = {
    "nlp": {
        "pipeline": [
            {
                "factory": "textcat",
                "architecture": "simple_cnn",
                "exclusive_classes": True,
            }
        ]
    }
}

# Load a blank spaCy model
nlp = spacy.blank("en")

config = {
    "exclusive_classes": True,
    "model": DEFAULT_SINGLE_TEXTCAT_MODEL,
}
textcat = nlp.create_pipe("textcat", config=config)
textcat.add_label("PRODUCTS")
textcat.add_label("PROJECTS")
textcat.add_label("COMPANIES")
textcat.add_label("PLANS")
textcat.add_label("OTHER")
nlp.add_pipe(textcat)

# Add the text classification pipeline
textcat = nlp.add_pipe("textcat", config={"exclusive_classes": True, "architecture": "simple_cnn"})

# Define the categories and their labels
categories = {category: idx for idx, category in enumerate(categories)}

# Preprocess the text to get sentences
nlp_for_sentences = spacy.load("en_core_web_sm")
doc = nlp_for_sentences(text)
sentences = [sent.text for sent in doc.sents]

# Categorize sentences using the trained classifier
results = {key: [] for key in categories}
for doc in sentences:
    category = doc.cats
    sorted_categories = sorted(category.items(), key=lambda x: x[1], reverse=True)
    top_category = sorted_categories[0][0]
    results[top_category].append(doc.text)

# Generate summaries for each category
summaries = {}
for category, sentences in results.items():
    prompt = f"Please provide a summary of the following sentences about {category}: {' '.join(sentences)}"
    summary = generate_response(prompt)
    summaries[category] = summary
    with open(f"{category}_summary.txt", "w") as output_file:
        output_file.write(summary)
    logging.info(prompt)

# Print the summaries for verification
for category, summary in summaries.items():
    print(f"Category: {category}\nSummary: {summary}\n")
    logging.info(category)


# Prepare the training data
train_data = []
for category, sentences in example_sentences.items():
    for sentence in sentences:
        cats = {cat: 1 if cat == category else 0 for cat in categories}
        train_data.append((sentence, {"cats": cats}))

# Train the text classifier
optimizer = nlp.begin_training()
batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
for epoch in range(10):
    random.shuffle(train_data)
    losses = {}
    for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)

# Save the trained model
output_dir = Path("trained_model")
if not output_dir.exists():
    output_dir.mkdir()
nlp.to_disk(output_dir)

# Load the trained model for classification
nlp_trained = spacy.load(output_dir)

# Read the content of the file
with open("paste_conversion_here.txt", "r") as file:
    text = file.read()

# Preprocess the text
sentences = list(nlp_trained.pipe(text.split("\n")))

# Categorize sentences using the trained classifier
results = {key: [] for key in categories}
for doc in sentences:
    category = doc.cats
    sorted_categories = sorted(category.items(), key=lambda x: x[1], reverse=True)
    top_category = sorted_categories[0][0]
    results[top_category].append(doc.text)

# Save the categorized sentences into separate files
for category, sentences in results.items():
    with open(f"{category}_sentences.txt", "w") as output_file:
        for sentence in sentences:
            output_file.write(f"{sentence}\n")

# Print the results for verification
for category, sentences in results.items():
    print(f"Category: {category}")
    for sentence in sentences:
        print(f" {sentence}")
        logging.info(sentence)

# Generate summaries for each category
summaries = {}
for category, sentences in results.items():
    prompt = f"Please provide a summary of the following sentences about {category}: {' '.join(sentences)}"
    summary = generate_response(prompt)
    summaries[category] = summary
    with open(f"{category}_summary.txt", "w") as output_file:
        output_file.write(summary)
    logging.info(prompt)

# Print the summaries for verification
for category, summary in summaries.items():
    print(f"Category: {category}\nSummary: {summary}\n")
    logging.info(category)

# Save the categorized sentences into separate files
for category, sentences in results.items():
    with open(f"{category}_sentences.txt", "w") as output_file:
        for sentence in sentences:
            output_file.write(f"{sentence}\n")
    # Save the summaries into separate files
    with open(f"specific_folder/{category}_summary.txt", "w") as output_file:
        output_file.write(summaries[category])

# Print the results for verification
for category, sentences in results.items():
    print(f"Category: {category}")
    for sentence in sentences:
        print(f" {sentence}")
        logging.info(sentence)
    with open(f"specific_folder/{category}_sentences.txt", "r") as input_file:
        print(f" Sentences: {input_file.read()}")
    with open(f"specific_folder/{category}_summary.txt", "r") as input_file:
        print(f" Summary: {input_file.read()}")


