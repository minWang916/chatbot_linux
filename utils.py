import chainlit as cl
import tiktoken

MAX_TOKEN_LIMIT = 4096

MODEL_COSTS = {
    "gpt-3.5-turbo": {"input": 0.000003, "output": 0.000006},  
    "gpt-4": {"input": 0.0000003, "output": 0.000012},  
}

def count_tokens(messages, model):
    # Load the tokenizer for the specified model
    encoding = tiktoken.encoding_for_model(model)
    tokens = 0

    if type(messages) == str:
        # Encode the entire message if it is a single string
        tokens += len(encoding.encode(messages))
        return tokens
    else:
        for message in messages:
            # Encode the role and content separately and count tokens in each chat history entry
            tokens += len(encoding.encode(message["role"])) + len(encoding.encode(message["content"]))
    return tokens

def trim_chat_history(chat_history, model):
    while count_tokens(chat_history, model) > MAX_TOKEN_LIMIT:
        # Remove the oldest message (first element) until within the limit
        chat_history.pop(0)
    return chat_history

def create_cost_summary(input, output, model):
    input_token_count = count_tokens(input, model)
    output_token_count = count_tokens(output, model)
    
    print("Current model: ", model)
    input_cost = input_token_count * MODEL_COSTS[model]["input"]
    output_cost = output_token_count * MODEL_COSTS[model]["output"]
    total_cost = input_cost + output_cost

    cost_summary = (
        f"\n\n**Cost Statistics:**\n"
        f"- Input tokens: {input_token_count}\n"
        f"- Output tokens: {output_token_count}\n"
        f"- Total cost: ${total_cost:.7f}"
    )
    
    return cost_summary