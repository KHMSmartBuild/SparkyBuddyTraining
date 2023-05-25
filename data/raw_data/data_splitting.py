import pandas as pd
from sklearn.model_selection import train_test_split

# Load preprocessed data
data = pd.read_csv('preprocessed_data.csv')

# Split data into training, validation, and test sets
train_data, val_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Save training, validation, and test sets to files
train_data.to_csv('train_data.csv', index=False)
val_data.to_csv('val_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)
