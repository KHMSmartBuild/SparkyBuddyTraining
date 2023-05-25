import pandas as pd
import tensorflow as tf

# Load training data
train_data = pd.read_csv('train_data.csv')

# Define model architecture
num_features = 10
num_classes = 2
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=16, activation='relu', input_shape=(num_features,)),
    tf.keras.layers.Dense(units=8, activation='relu'),
    tf.keras.layers.Dense(units=num_classes, activation='softmax')
])

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train model
num_epochs = 10
batch_size = 32
model.fit(train_data, epochs=num_epochs, batch_size=batch_size)

# Save trained model to file
model.save('model.h5')
