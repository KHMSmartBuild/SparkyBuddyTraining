from functions_lib import Functions

def get_function_description(import_line):
    return Functions.get(import_line, "Description not found")

import_line = "from .function_explanations import generate_function_explanations"
print(get_function_description(import_line))  # Output: Generate function explanations.
