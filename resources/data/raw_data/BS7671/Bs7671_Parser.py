import re
import json

# Load the entire plain text content of BS7671
with open('bs7671.txt', 'r') as f:
    content = f.read()

# Define regular expression patterns for sections and subsections
section_pattern = re.compile(r'^"(\d+)",(.+)$', re.MULTILINE)
subsection_pattern = re.compile(r'^"(\d+\.\d+)",(.+)$', re.MULTILINE)

# Parse the text and build the data structure
structured_data = []

for section_match in section_pattern.finditer(content):
    section_number, section_title = section_match.groups()
    section_data = {
        "section_number": section_number.strip(),
        "section_title": section_title.strip('"'),
        "section_content": []
    }

    # Find the content between the current section and the next section
    section_end = section_match.end()
    next_section = section_pattern.search(content, pos=section_end)
    if next_section:
        section_content = content[section_end:next_section.start()]
    else:
        section_content = content[section_end:]

    # Parse the subsections and their content
    for subsection_match in subsection_pattern.finditer(section_content):
        subsection_number, subsection_title = subsection_match.groups()
        subsection_data = {
            "sub_section_number": subsection_number.strip(),
            "sub_section_title": subsection_title.strip('"'),
            "sub_section_content": []  # Add logic to extract the content of each subsection
        }

        section_data["section_content"].append(subsection_data)

    structured_data.append(section_data)

# Convert the data structure to JSON and save it to a file
with open('bs7671.json', 'w') as f:
    json.dump(structured_data, f, indent=2)
