# Script name : image_prompt_keywords.py
# location = gui\sparky\image_prompt_keywords.py
# accessable from Libraries = #TODO: Add to libraries 


image_prompt_keywords = {
    "image": "# Refers to the image as a whole",
    "generate": "# Instructs DALL-E to create or produce an image",
    "visualize": "# Instructs DALL-E to represent an idea or concept visually",
    "description": "# Provides a textual description for DALL-E to base the image on",
    "scene": "# Refers to the overall setting or environment in the image",
    "context": "# Provides additional information to help DALL-E understand the subject",
    "create": "# Instructs DALL-E to make an original image",
    "render": "# Instructs DALL-E to produce a detailed or high-quality image",
    "transform": "# Instructs DALL-E to change or modify an existing image or concept",
    "artistic": "# Indicates that the image should have a creative or unique style",
    "style": "# Specifies the artistic or visual style for the image",
    "objects": "# Refers to specific items or elements within the image",
    "colors": "# Indicates the color palette or specific colors to use",
    "composition": "# Refers to the arrangement or layout of elements in the image",
    "texture": "# Refers to the surface quality or appearance of objects in the image",
    "perspective": "# Indicates the point of view or angle from which the image is seen",
    "lighting": "# Refers to the illumination or brightness in the image",
    "abstract": "# Indicates that the image should be non-representational or conceptual",
    "photorealistic": "# Specifies that the image should appear highly detailed and realistic",
    "synthesis": "# Instructs DALL-E to combine or merge multiple ideas or concepts",
}

# To use a keyword from the dictionary, access it by its key like this:
example_keyword = image_prompt_keywords["visualize"]
print(example_keyword)
