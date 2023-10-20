from typing import List, Callable, Optional
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

# Define a function to run the agent chain with retries
def run_chain_with_retries(agent_chain: AgentExecutor, retries: int, **agent_run_kwargs) -> str:
    exception = None
    for _ in range(retries):
        try:
            return agent_chain.run(**agent_run_kwargs)
        except Exception as e:
            exception = e
    raise exception

# Define a function to run the knowledge agent
def run_knowledge_agent(
    gather_prompt: str,
    build_web_agent_func: Callable[[], AgentExecutor],
    deep_dive_topics: int,
    deep_dive_rounds: int,
    retries: Optional[int] = 3,
    chat_model: Optional[ChatGPT] = None,
    **prompt_args
) -> List[str]:
    if chat_model is None:
        chat_model = get_default_chat_model(default_chat_model_options)

    initial_agent_chain = build_web_agent_func()
    initial_info_chunk = run_chain_with_retries(
        initial_agent_chain,
        retries,
        input=knowledge_agent_constants.INITIAL_WEB_AGENT_PROMPT.format(gather_prompt=gather_prompt),
    )
    knowledge_chunks = [initial_info_chunk]

    for _ in range(deep_dive_rounds):
        round_knowledge = "\n\n".join(knowledge_chunks)
        deep_dive_area_prompt = knowledge_agent_constants.DEEP_DIVE_LIST_PROMPT.format(
            num_topics=deep_dive_topics,
            gather_prompt=gather_prompt,
            current_knowledge=round_knowledge,
            **prompt_args
        )
        deep_dive_list = chat_model(deep_dive_area_prompt)
        try:
            deep_dive_areas = [v.split(". ", 1)[1] for v in deep_dive_list.strip().split("\n")]
        except IndexError:
            print("Failed to parse topics", deep_dive_list)
            break

        for deep_dive_topic in deep_dive_areas:
            deep_dive_web_agent_prompt = knowledge_agent_constants.DEEP_DIVE_WEB_AGENT_PROMPT.format(
                gather_prompt=gather_prompt,
                current_knowledge=round_knowledge,
                deep_dive_topic=deep_dive_topic,
            )
            agent_chain = build_web_agent_func()
            info_chunk = run_chain_with_retries(
                agent_chain,
                retries,
                input=deep_dive_web_agent_prompt,
            )
            knowledge_chunks.append(info_chunk)

    return knowledge_chunks
