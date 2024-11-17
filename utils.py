import chainlit as cl
import tiktoken

MAX_TOKEN_LIMIT = 4096
MODEL = "gpt-4"

MODEL_COSTS = {
    "gpt-3.5": {"input": 0.003, "output": 0.006},  
    "gpt-4": {"input": 0.0003, "output": 0.0012},  
}

def count_tokens(messages, model=MODEL):
    # Load the tokenizer for the specified model
    encoding = tiktoken.encoding_for_model(model)
    tokens = 0

    for message in messages:
        # Encode the role and content separately and count tokens
        tokens += len(encoding.encode(message["role"])) + len(encoding.encode(message["content"]))
    return tokens

def trim_chat_history(chat_history, model=MODEL):
    while count_tokens(chat_history, model=model) > MAX_TOKEN_LIMIT:
        # Remove the oldest message (first element) until within the limit
        chat_history.pop(0)
    return chat_history