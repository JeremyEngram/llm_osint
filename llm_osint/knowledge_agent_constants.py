from transformers import ChatGPT

# Define your default chat model options
default_chat_model_options = {
    "model_name": "gpt-4-0613",
    "max_response_length": 100,
    "temperature": 0.7,
}

def get_default_chat_model(options) -> ChatGPT:
    chat = ChatGPT.from_pretrained(options["model_name"])
    chat.default_max_response_length = options["max_response_length"]
    chat.temperature = options["temperature"]
    return chat

# Define your prompts
SUMMARY_TASK_PROMPT = "Then list all the information you have gathered and where these details were gathered from. Be VERY detailed and list as much information as possible."

INITIAL_WEB_AGENT_PROMPT = """
{gather_prompt}

{SUMMARY_TASK_PROMPT}
"""

DEEP_DIVE_LIST_PROMPT = """
Given these details about {name} and search and webpage reading abilities, create a list of {num_topics} areas to deep dive into to better "{gather_prompt}".

Format the areas as a numbered list. Respond only with the list.

Details:
{current_knowledge}
"""

DEEP_DIVE_WEB_AGENT_PROMPT = """
{gather_prompt}

Here's what you already know:
{current_knowledge}

{SUMMARY_TASK_PROMPT}

For now, specifically ONLY look into: {deep_dive_topic}
"""

# Example usage:
default_chat_model = get_default_chat_model(default_chat_model_options)

# Using the prompts
initial_web_agent_prompt = INITIAL_WEB_AGENT_PROMPT.format(gather_prompt="Your Gather Prompt")
deep_dive_list_prompt = DEEP_DIVE_LIST_PROMPT.format(
    name="Name",
    num_topics=5,
    gather_prompt="Your Gather Prompt",
    current_knowledge="Current Knowledge",
)
deep_dive_web_agent_prompt = DEEP_DIVE_WEB_AGENT_PROMPT.format(
    gather_prompt="Your Gather Prompt",
    current_knowledge="Current Knowledge",
    deep_dive_topic="Deep Dive Topic",
)

# Generate responses using the chat model
response1 = default_chat_model(initial_web_agent_prompt)
response2 = default_chat_model(deep_dive_list_prompt)
response3 = default_chat_model(deep_dive_web_agent_prompt)
