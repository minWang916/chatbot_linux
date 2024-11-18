"""
utils.py
=========
Provides utility functions and constants to support the chatbot's operations.

Features:
- Token counting for OpenAI's language models.
- Trimming chat history to fit within token limits.
- Generating cost summaries based on token usage.

Constants:
- MAX_TOKEN_LIMIT (int): Maximum number of tokens allowed in a conversation context.
- MODEL_COSTS (dict): Per-token input and output costs for supported models.
"""
import chainlit as cl
import tiktoken

# Constants
MAX_TOKEN_LIMIT = 8000

MODEL_COSTS = {
    "gpt-3.5-turbo": {"input": 0.000003, "output": 0.000006},  
    "gpt-4": {"input": 0.0000003, "output": 0.000012},  
}

def count_tokens(messages, model):
    """
    Count the total number of tokens in a conversation or single message.

    Parameters:
    - messages (str | list): A string or list of dictionaries representing the conversation history.
      If a list, each dictionary should contain:
        - 'role' (str): The role of the sender (e.g., "user", "assistant").
        - 'content' (str): The message content.
    - model (str): The name of the OpenAI model (e.g., "gpt-3.5-turbo", "gpt-4").

    Returns:
    - int: The total number of tokens in the given input.

    Example:
    >>> count_tokens("Hello, world!", "gpt-3.5-turbo")
    3
    >>> count_tokens([{"role": "user", "content": "Hi"}], "gpt-3.5-turbo")
    4
    """
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
    """
    Trim chat history to ensure the token count is within the allowed limit.

    Parameters:
    - chat_history (list): A list of dictionaries representing the conversation history.
    - model (str): The name of the OpenAI model (e.g., "gpt-3.5-turbo", "gpt-4").

    Returns:
    - list: The trimmed chat history.

    Note:
    - This function removes the oldest messages (first elements) until the total token count
      is less than or equal to MAX_TOKEN_LIMIT.

    Example:
    >>> chat_history = [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}]
    >>> trim_chat_history(chat_history, "gpt-3.5-turbo")
    [{"role": "assistant", "content": "Hello"}]
    """
    while count_tokens(chat_history, model) > MAX_TOKEN_LIMIT:
        # Remove the oldest message (first element) until within the limit
        chat_history.pop(0)
    return chat_history

def create_cost_summary(input, output, model):
    """
    Generate a summary of the cost statistics for a given conversation.

    Parameters:
    - input (str | list): The input text or conversation history.
    - output (str): The assistant's response text.
    - model (str): The name of the OpenAI model (e.g., "gpt-3.5-turbo", "gpt-4").

    Returns:
    - str: A formatted cost summary including token counts and total cost.

    Example:
    >>> input = [{"role": "user", "content": "Hi"}]
    >>> output = "Hello!"
    >>> create_cost_summary(input, output, "gpt-3.5-turbo")
    '\n\n**Cost Statistics:**\n- Input tokens: 4\n- Output tokens: 2\n- Total cost: $0.00002'
    """
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