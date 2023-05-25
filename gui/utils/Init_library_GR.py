import os
import re

def generate_imports(base_path):
    imports = []

    for root, dirs, files in os.walk(base_path):
        if "myenv" in root.split(os.sep) or "databases" in root.split(os.sep):
            continue  # Skip the directory if it's part of the 'myenv' or 'databases' folders

        for file in files:
            if file.endswith(".py") and file != "__init__.py" and "database_functions" not in file:
                subdir = root.replace(base_path, "").lstrip(os.sep)
                module_path = subdir.replace(os.sep, ".")

                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with open(os.path.join(root, file), "r", encoding="ISO-8859-1") as f:
                        content = f.read()

                matches = re.findall(r"^(?:class|def)\s+(\w+)", content, re.MULTILINE)

                for match in matches:
                    import_line = f"from {module_path}.{file[:-3]} import {match}"
                    imports.append(import_line)

    return imports

if __name__ == "__main__":
    current_path = os.getcwd()
    imports = generate_imports(current_path)

    with open(os.path.join(current_path, "__init__.py"), "w") as f:
        f.write(f"# {current_path} folder libraries\n")
        f.write("# __init__.py\n\n")

        for import_line in imports:
            f.write(import_line + "\n")
