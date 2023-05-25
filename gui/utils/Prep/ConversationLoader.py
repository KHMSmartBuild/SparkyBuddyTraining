import json

class ConversationLoader:
    def __init__(self):
        self.conversations = []

    def load_conversations(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        self.conversations.extend(data["conversations"])

    def process_conversations(self):
        processed_conversations = []
        for conversation in self.conversations:
            processed_conversation = []
            for message in conversation:
                processed_conversation.append((message["role"], message["content"]))
            processed_conversations.append(processed_conversation)
        return processed_conversations

# Example usage:

# Create a ConversationLoader instance
loader = ConversationLoader()

# Load and process the conversation data from the JSON file
loader.load_conversations("convo-1.js")
processed_conversations = loader.process_conversations()

# If you want to load more conversation files, just call `load_conversations` again:
# loader.load_conversations("another_file.js")

# Print the first conversation
for role, content in processed_conversations[0]:
    print(f"{role}: {content}")
