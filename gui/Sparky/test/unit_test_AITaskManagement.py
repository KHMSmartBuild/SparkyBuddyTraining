import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication
from gui.openai import AITaskManagement


class TestAITaskManagement(unittest.TestCase):
    def setUp(self):
        """Set up the test environment.

        Creates a QApplication and an AITaskManagement instance for testing purposes.

        Args:
            self: The test class instance.

        Returns:
            None.
        """
        self.app = QApplication([])
        self.ai_task_manager = AITaskManagement()

    def test_load_data(self):
        """
        Test the load_data function of the ai_task_manager object to ensure that it
        properly loads the data and returns non-None values for X_train, X_test,
        y_train, and y_test.

        Args:
            self (object): The ai_task_manager object to be tested.

        Returns:
            None
        """
        self.ai_task_manager.load_data()
        self.assertIsNotNone(self.ai_task_manager.X_train)
        self.assertIsNotNone(self.ai_task_manager.X_test)
        self.assertIsNotNone(self.ai_task_manager.y_train)
        self.assertIsNotNone(self.ai_task_manager.y_test)

    def test_train_model(self):
        """
    Test the function that trains the model with different algorithms.

    The function sets the model combo box to "Random Forest" and trains the model. It then asserts that the model is not None.
    The same process is repeated for "Support Vector Machine" and "k-Nearest Neighbors" algorithms.

    Args:
        self: The object itself.

    Returns:
        None
    """
        self.ai_task_manager.model_combo_box.setCurrentText("Random Forest")
        self.ai_task_manager.train_model()
        self.assertIsNotNone(self.ai_task_manager.model)

        self.ai_task_manager.model_combo_box.setCurrentText("Support Vector Machine")
        self.ai_task_manager.train_model()
        self.assertIsNotNone(self.ai_task_manager.model)

        self.ai_task_manager.model_combo_box.setCurrentText("k-Nearest Neighbors")
        self.ai_task_manager.train_model()
        self.assertIsNotNone(self.ai_task_manager.model)

    def test_evaluate_model(self):
        """
    Test the evaluation of a trained model by setting the model combo box to
    'Random Forest', training the model, evaluating it, and checking that the
    result label's text is not 'No model has been trained yet.'.
    """
        self.ai_task_manager.model_combo_box.setCurrentText("Random Forest")
        self.ai_task_manager.train_model()
        self.ai_task_manager.evaluate_model()
        self.assertNotEqual(self.ai_task_manager.result_label.text(), "No model has been trained yet.")

    def test_test_model(self):
        """
    Set the model combo box of the AI task manager to "Random Forest", train the model
    and test it. Check that the result label text is not equal to "No model has been trained yet."
    """
        self.ai_task_manager.model_combo_box.setCurrentText("Random Forest")
        self.ai_task_manager.train_model()
        self.ai_task_manager.test_model()
        self.assertNotEqual(self.ai_task_manager.result_label.text(), "No model has been trained yet.")

    def test_run_inference(self):
        """
    Test the run inference functionality of the AI task manager.

    This function sets the model combo box to "Random Forest", trains the model, and runs inference. It then asserts that the result label text is not equal to "No model has been trained yet.".
    """
        self.ai_task_manager.model_combo_box.setCurrentText("Random Forest")
        self.ai_task_manager.train_model()
        self.ai_task_manager.run_inference()
        self.assertNotEqual(self.ai_task_manager.result_label.text(), "No model has been trained yet.")

    def test_visualize_data(self):
        """
    Test the visualize_data function of the AI task manager.

    This function mocks the seaborn and matplotlib.pyplot modules and calls the
    visualize_data function of the AI task manager. It then asserts that the pairplot
    function of seaborn was called once, and that the show function of matplotlib.pyplot
    was called once as well.

    :param self: The instance of the test class.
    :return: None
    """
        # function body
        sns = MagicMock()
        plt = MagicMock()
        self.ai_task_manager.visualize_data()
        sns.pairplot.assert_called_once()
        plt.show.assert_called_once()

    def test_show_classification_report(self):
        self.ai_task_manager.model_combo_box.setCurrentText("Random Forest")
        self.ai_task_manager.train_model()
        self.ai_task_manager.show_classification_report()
        self.assertNotEqual(self.ai_task_manager.result_label.text(), "No model has been trained yet.")

    def tearDown(self):
        self.ai_task_manager.close()
        del self.ai_task_manager
        del self.app

if __name__ == '__main__':
    unittest.main()
