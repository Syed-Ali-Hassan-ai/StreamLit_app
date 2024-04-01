import json
from langchain.schema.messages import HumanMessage, AIMessage
from datetime import datetime
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)
    
def save_chat_history_json(chat_history, file_path):
    with open(file_path, "w") as f:
        # If the chat history is already a list of dictionaries, just dump it directly to JSON
        json.dump(chat_history, f)

def load_chat_history_json(file_path):
    with open(file_path, "r") as f:
        json_data = json.load(f)
        messages = [HumanMessage(**message) if message["type"] == "human" else AIMessage(**message) for message in json_data]
        return messages

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")