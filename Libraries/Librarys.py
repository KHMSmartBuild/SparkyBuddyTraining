# Data library

class DataLibrary:
    def __init__(self, train_data, test_data, validation_data, metadata):
        self.train_data = train_data
        self.test_data = test_data
        self.validation_data = validation_data
        self.metadata = metadata

# Models library

class ModelsLibrary:
    def __init__(self, neural_networks, decision_trees, support_vector_machines, other_models):
        self.neural_networks = neural_networks
        self.decision_trees = decision_trees
        self.support_vector_machines = support_vector_machines
        self.other_models = other_models

    def train_models(self, data_library):
        #TODO Code for training models

        def evaluate_models(self, data_library, evaluation_library):
            #TODO Code for evaluating models

            # Evaluation library

class EvaluationLibrary:
    def __init__(self, accuracy_metrics, loss_functions, other_metrics):
        self.accuracy_metrics = accuracy_metrics
        self.loss_functions = loss_functions
        self.other_metrics = other_metrics

# Utils library

class UtilsLibrary:
    def __init__(self, load_data_functions, preprocess_data_functions, visualization_functions, other_utility_functions):
        self.load_data_functions = load_data_functions
        self.preprocess_data_functions = preprocess_data_functions
        self.visualization_functions = visualization_functions
        self.other_utility_functions = other_utility_functions
