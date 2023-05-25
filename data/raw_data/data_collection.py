import pandas as pd

# Load data
data = pd.read_csv('data.csv')

# Preprocess data

# Save preprocessed data to file
data.to_csv('preprocessed_data.csv', index=False)
