import os

def create_new_script(script_name, location, function_description):
    template = f"""# Script name : {script_name}
# location = {location}
# Function = {function_description}
# accessible from Libraries =

class ClassName:
    def method_name(self, parameter1, parameter2):
        \"\"\"{function_description}

        :param parameter1: Description of parameter1
        :param parameter2: Description of parameter2
        :return: Description of the return value
        \"\"\"
        # TODO: Implement the method logic
        pass
    """

    with open(os.path.join(location, script_name + '.py'), 'w') as script_file:
        script_file.write(template)

if __name__ == '__main__':
    script_name = input("Enter script name: ")
    location = input("Enter script location: ")
    function_description = input("Enter function description: ")

    create_new_script(script_name, location, function_description)

