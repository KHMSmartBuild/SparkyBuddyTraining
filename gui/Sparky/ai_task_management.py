# Script name : ai_task_management.py
#Location = gui\Sparky\ai_task_management.py
# Author: KHM Smartbuild
# Purpose: 
"""
AI Task Management class for managing machine learning tasks.

This class provides a graphical user interface for selecting and training machine learning models, testing the models on a 
test dataset, running inference on new data, and saving and loading trained models.

The class uses the PyQt5 library for creating the user interface and the scikit-learn library for training and testing 
machine learning models.
"""
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild

import json
import joblib
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QInputDialog, QComboBox, QApplication, QWidget, QMessageBox, QProgressBar
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns
import matplotlib.pyplot as plt

class AITaskManagement(QWidget):
    """
    AITaskManagement class for managing machine learning tasks.

    Attributes:
        layout (QVBoxLayout): The main layout for the user interface.
        model_selection_layout (QHBoxLayout): The layout for selecting the machine learning model.
        model_label (QLabel): The label for the model selection dropdown.
        model_combo_box (QComboBox): The dropdown for selecting the machine learning model.
        buttons_layout (QHBoxLayout): The layout for the train, test, and inference buttons.
        train_button (QPushButton): The button for training the machine learning model.
        test_button (QPushButton): The button for testing the machine learning model.
        inference_button (QPushButton): The button for running inference with the machine learning model.
        result_label (QLabel): The label for displaying the results of the machine learning tasks.
        X_train (ndarray): The training features.
        X_test (ndarray): The testing features.
        y_train (ndarray): The training labels.
        y_test (ndarray): The testing labels.
        model (RandomForestClassifier): The trained machine learning model.

    Methods:
        load_data(): Loads the Iris dataset and creates a train-test split.
        evaluate_model(): Evaluates the trained machine learning model's accuracy on the test dataset and displays the 
            result.
        train_model(): Trains the selected machine learning model on the training dataset and displays the result.
        test_model(): Tests the selected machine learning model on the test dataset and displays the result.
        run_inference(): Runs inference with the selected machine learning model on new data and displays the result.
        save_model(): Saves the trained machine learning model to a file.
        load_model(): Loads a saved machine learning model from a file.
    """

    def __init__(self):
        """
        Initializes the AITaskManagement object with the main user interface layout and widgets.
        """

        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Model selection
        self.model_selection_layout = QHBoxLayout()
        self.model_label = QLabel("Select Model:")
        self.model_combo_box = QComboBox()
        self.model_combo_box.setEditable(True)
        self.model_combo_box.addItem("Random Forest")
        self.model_combo_box.addItem("Support Vector Machine")
        self.model_combo_box.addItem("k-Nearest Neighbors")

        self.model_selection_layout.addWidget(self.model_label)
        self.model_selection_layout.addWidget(self.model_combo_box)

        self.layout.addLayout(self.model_selection_layout)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()

        # Select dataset button
        self.dataset_button = QPushButton("Select Dataset")
        self.dataset_button.clicked.connect(self.select_dataset)
        self.buttons_layout.addWidget(self.dataset_button)

        # Train, Test, and Inference buttons
        self.train_button = QPushButton("Train Model")
        self.train_button.clicked.connect(self.train_model)
        self.test_button = QPushButton("Test Model")
        self.test_button.clicked.connect(self.test_model)
        self.inference_button = QPushButton("Run Inference")
        self.inference_button.clicked.connect(self.run_inference)

        self.buttons_layout.addWidget(self.train_button)
        self.buttons_layout.addWidget(self.test_button)
        self.buttons_layout.addWidget(self.inference_button)

        self.result_label = QLabel("Results will be displayed here.")
        self.layout.addWidget(self.result_label)
        self.layout.addLayout(self.buttons_layout)

        # Add a progress bar to the layout
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        # visualization
        self.visualize_data_button = QPushButton("Visualize Data")
        self.visualize_data_button.clicked.connect(self.visualize_data)
        self.buttons_layout.addWidget(self.visualize_data_button)

        # Report
        self.report_button = QPushButton("Show Classification Report")
        self.report_button.clicked.connect(self.show_classification_report)
        self.buttons_layout.addWidget(self.report_button)

        # Load data
        self.load_data()

    def select_dataset(self):
        """
        Shows a dialog box to select a dataset and loads the corresponding data if the user confirms.

        :return: None
        """
        dataset_names = ["Iris", "Another Dataset"]
        dataset, ok = QInputDialog.getItem(self, "Select Dataset", "Dataset:", dataset_names, 0, False)
        if ok:
            if dataset == "Iris":
                self.load_data()
            elif dataset == "Another Dataset":
                self.load_another_dataset()

    def load_data(self):
            """
            Loads the Iris dataset and creates a train-test split.
            """
            iris = load_iris()
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(iris.data, iris.target, test_size=0.2)

    def train_model(self):
            """
                {Python} Trains a machine learning model based on the user's selection.

                    Args: self: The instance of the class calling the function.

                    Returns: None.

                    Raises: None.

                    Notes: - This function is triggered by a button or menu in a GUI application. 
                    - The function retrieves the user's selected model from a combo box.
                    - If the selected model is "Random Forest", the function initializes a random forest classifier with 100 estimators.
                    - If the selected model is "Support Vector Machine", 
                    the function initializes a support vector machine classifier with a linear kernel and C=1. 
                    - If the selected model is "k-Nearest Neighbors", the function initializes a k-nearest neighbors classifier with k=3. 
                    - The function fits the model with training data stored in self.Xtrain and self.ytrain. 
                    - The function updates a progress bar and a result label in the GUI to indicate that the model has been trained successfully.
            """
            selected_model = self.model_combo_box.currentText()
            print(f"Training {selected_model}...")

            if selected_model == "Random Forest":
                self.model = RandomForestClassifier(n_estimators=100)
            elif selected_model == "Support Vector Machine":
                self.model = SVC(kernel='linear', C=1)
            elif selected_model == "k-Nearest Neighbors":
                self.model = KNeighborsClassifier(n_neighbors=3)

            self.model.fit(self.X_train, self.y_train)
            self.result_label.setText(f"Model {selected_model} trained successfully.")
            self.progress_bar.setValue(50)


    
    def evaluate_model(self):
        """
        Evaluates the trained machine learning model's accuracy on the test dataset and displays the result.
        """

        if hasattr(self, 'model'):
            with open('data.json', 'r') as f:
                data = json.load(f)
            X_test = np.array(data['X_test'])
            y_test = np.array(data['y_test'])

            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Model accuracy: {accuracy:.2f}")
            self.result_label.setText(f"Model accuracy: {accuracy:.2f}")
        else:
            print("No model has been trained yet.")
            self.result_label.setText("No model has been trained yet.")

    
    def test_model(self):
        """
        Tests the selected machine learning model on the test dataset and displays the result.
        """

        selected_model = self.model_combo_box.currentText()
        print(f"Testing {selected_model}...")
        self.evaluate_model()

    def run_inference(self):
        """
        Runs inference with the selected machine learning model on new data and displays the result.
        """

        selected_model = self.model_combo_box.currentText()
        print(f"Running inference with {selected_model}...")

        petal_length, petal_width, sepal_length, sepal_width, ok = QInputDialog.getText(self, "Input Dialog", "Enter petal length, petal width, sepal length, and sepal width separated by commas:")
        if ok:
            new_data = np.array([[float(x) for x in petal_length.split(",")], [float(x) for x in petal_width.split(",")], [float(x) for x in sepal_length.split(",")], [float(x) for x in sepal_width.split(",")]])
            prediction = self.model.predict(new_data.T)
            print(f"Done! Prediction: {prediction[0]}")
            self.result_label.setText(f"Prediction: {prediction[0]}")

    def visualize_data(self):
        """
        Visualize the training data using a pairplot with KDE diagonal plots.

        Arguments:
        - self: an instance of a class with an attribute X_train, a 2D array-like object with four columns
        representing sepal length, sepal width, petal length, and petal width, respectively.

        Returns:
        - None
        """
        sns.pairplot(pd.DataFrame(self.X_train, columns=['sepal length', 'sepal width', 'petal length', 'petal width']),
                    diag_kind='kde')
        plt.show()

    def show_classification_report(self):
        """
        Generate and display a classification report and confusion matrix based on the model's predictions.

        If the model has not yet been trained, display an appropriate message.

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        if hasattr(self, 'model'):
            y_pred = self.model.predict(self.X_test)
            report = classification_report(self.y_test, y_pred)
            print("Classification report:")
            print(report)

            cm = confusion_matrix(self.y_test, y_pred)
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
            plt.xlabel('Predicted label')
            plt.ylabel('True label')
            plt.title('Confusion Matrix')
            plt.show()

        else:
            print("No model has been trained yet.")
            self.result_label.setText("No model has been trained yet.")


    def save_model(self):
        """
        Saves the trained machine learning model to a file.
        """

        if hasattr(self, 'model'):
            joblib.dump(self.model, 'trained_model.pkl')
            print("Model saved.")
            self.result_label.setText("Model saved.")
        else:
            print("No model to save.")
            self.result_label.setText("No model to save.")

    def load_model(self):
        """
        Loads a saved machine learning model from a file.
        """

        try:
            self.model = joblib.load('trained_model.pkl')
            print("Model loaded.")
            self.result_label.setText("Model loaded.")
        except FileNotFoundError:
            print("No saved model found.")
            self.result_label.setText("No saved model found.")

    def evaluate_model(self):
        """
        Evaluates the trained machine learning model's accuracy on the test dataset and displays the result.
        """

        if hasattr(self, 'model'):
            with open('data.json', 'r') as f:
                data = json.load(f)
            X_test = np.array(data['X_test'])
            y_test = np.array(data['y_test'])

            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Model accuracy: {accuracy:.2f}")
            self.result_label.setText(f"Model accuracy: {accuracy:.2f}")
        else:
            print("No model has been trained yet.")
            self.result_label.setText("No model has been trained yet.")


    # Define the AITaskManagement class that inherits from QWidget
    def closeEvent(self, event):
        """
        Overrides the default closeEvent method to prompt the user to save the trained model before closing the application.
        """

        reply = QMessageBox.question(self, "Save Model", "Do you want to save the trained model?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.save_model()
        elif reply == QMessageBox.Cancel:
            event.ignore()
        else:
            pass


if __name__ == '__main__':
    # Properly indented and formatted to run the application
    import sys

    app = QApplication(sys.argv)
    ex = AITaskManagement()
    ex.show()
    sys.exit(app.exec_())