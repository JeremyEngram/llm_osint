from transformers import ChatGPT

# Define default options
default_fast_llm_options = {
    "model_name": "gpt-3.5-turbo-16k-0613",
    "max_response_length": 100,  # Set your desired max response length
    "temperature": 0.7,
}

default_llm_options = {
    "model_name": "gpt-4-0613",
    "max_response_length": 100,  # Set your desired max response length
    "temperature": 0.7,
}

def get_default_chat_model(options) -> ChatGPT:
    chat = ChatGPT.from_pretrained(options["model_name"])
    chat.default_max_response_length = options["max_response_length"]
    chat.temperature = options["temperature"]
    return chat

# Create the default chat models
default_fast_chat_model = get_default_chat_model(default_fast_llm_options)
default_llm_chat_model = get_default_chat_model(default_llm_options)
