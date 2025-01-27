from typing import List, Optional, Union
from llm_osint import cache_utils, llm

@cache_utils.cache_func
def map(prompt: str, text: str, model: llm.LLMModel) -> str:
    return model.call_as_llm(prompt.format(text=text)

@cache_utils.cache_func
def reduce(prompt: str, texts: List[str], model: llm.LLMModel) -> str:
    return model.call_as_llm(prompt.format(texts="\n\n".join(texts)))

def map_reduce_texts(
    texts: List[str],
    map_prompt: Union[str, None],
    reduce_prompt: str,
    reduce_chunks: int,
    model: Optional[llm.LLMModel] = None,
) -> str:
    if model is None:
        model = llm.get_default_fast_llm()

    mapped_texts = [text if map_prompt is None else map(map_prompt, text, model) for text in texts]

    while len(mapped_texts) > 1:
        reduced_chunks = []
        while len(mapped_texts) > 0 and len(reduced_chunks) < reduce_chunks:
            reduced_chunks.append(mapped_texts.pop(0))
        mapped_texts.append(reduce(reduce_prompt, reduced_chunks, model))

    return mapped_texts[0]
