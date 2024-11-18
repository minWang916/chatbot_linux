"""
chat.py
=========
Handles the main chatbot logic, including model selection, chat session management, and response generation.

Features:
- Dynamic chat profile selection (GPT-3.5 or GPT-4).
- Initialization and management of chat sessions with contextual history.
- Integration with LlamaIndex for knowledge retrieval.
- Token management and response generation using OpenAI models.
- Cost calculation for tracking token usage.

Dependencies:
- Chainlit: Provides an interface for chatbot interactions.
- LlamaIndex: Handles document indexing and query retrieval.
- OpenAI: For GPT-3.5 and GPT-4 language models.
"""

import chainlit as cl
from chainlit.types import ThreadDict

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.core.callbacks import CallbackManager
from llama_index.core import Settings

from utils import count_tokens, trim_chat_history, create_cost_summary, MAX_TOKEN_LIMIT, MODEL_COSTS

from llama_index.core import (
    Settings,
    StorageContext,
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
)

# Load the LLM index from storage if it exists, otherwise create it
try:
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
except:
    documents = SimpleDirectoryReader("./data").load_data(show_progress=True)
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

@cl.set_chat_profiles
async def choose_profile():
    """
    Allow users to select a chatbot profile (GPT-3.5 or GPT-4).

    Returns:
    - list[cl.ChatProfile]: A list of available profiles, each with a name, description, and icon.

    Example:
    - GPT-3.5: For general-purpose queries.
    - GPT-4: For more advanced and complex interactions.
    """
    return [
        cl.ChatProfile(
            name="GPT-3.5",
            markdown_description="The underlying LLM model is **GPT-3.5**.",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="GPT-4",
            markdown_description="The underlying LLM model is **GPT-4**.",
            icon="https://picsum.photos/250",
        ),
    ]

@cl.on_chat_start
async def start_chat():
    """
    Initialize a new chat session by setting up the selected model and query engine.

    Workflow:
    1. Retrieve the selected chat profile (GPT-3.5 or GPT-4).
    2. Configure the OpenAI model and embedding settings.
    3. Create a query engine using LlamaIndex for document retrieval.
    4. Send an introductory message to the user.

    Example:
    "Hello! I'm GPT-4. You can ask me any question regarding Linux and Git commands."
    """
    model = cl.user_session.get("chat_profile")
    if model == "GPT-4":
        model = "gpt-4"
    if model == "GPT-3.5":
        model = "gpt-3.5-turbo"
    
    Settings.llm = OpenAI(
        model=model, temperature=0.5, max_tokens=1024, streaming=True
    )
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    Settings.context_window = 8192
    Settings.callback_manager = CallbackManager([cl.LlamaIndexCallbackHandler()])
    
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=5)
    cl.user_session.set("query_engine", query_engine)
    
    cl.user_session.set("chat_history", [])

    await cl.Message(
        author="Assistant", content="Hello! I'm " + model + ". You can ask me any question regarding Linux and Git command."
    ).send()
    
    
@cl.on_message
async def response_chat(message: cl.Message):
    """
    Process user messages and generate a response.

    Workflow:
    1. Retrieve chat history and append the user's message.
    2. Trim the chat history if it exceeds the token limit.
    3. Use the query engine to retrieve or generate a response.
    4. Calculate the token usage and cost summary.
    5. Send the assistant's response to the user.

    Parameters:
    - message (cl.Message): The user's input message.

    Returns:
    - None: Sends the response directly via Chainlit.

    Example:
    User: "What is the git clone command?"
    Assistant: "The `git clone` command is used to create a copy of a repository..."
    """
    query_engine = cl.user_session.get("query_engine")

    chat_history = cl.user_session.get("chat_history")
    chat_history.append({"role": "user", "content": message.content})

    if len(chat_history) == 1: 
        query_input = message.content
    else:
        # Prepare conversation history
        context = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in chat_history])
        query_input = f"Given the following conversation history:\n{context}\nAssistant:"

    # Count tokens
    model = cl.user_session.get("chat_profile")
    if model == "GPT-4":
        model = "gpt-4"
    if model == "GPT-3.5":
        model = "gpt-3.5-turbo"
    input_token_count = count_tokens(chat_history, model)

    # Trim history if necessary
    if input_token_count > MAX_TOKEN_LIMIT:
        chat_history = trim_chat_history(chat_history, model)
        print("Chat history trimmed.")

    # Query the model
    res = await cl.make_async(query_engine.query)(query_input)

    # Stream response from the model
    response_content = ""
    for token in res.response_gen:
        response_content += token
        

    # Add assistant response to chat history
    chat_history.append({"role": "assistant", "content": response_content})
    
    model_name = cl.user_session.get("chat_profile")
    cost_summary = create_cost_summary(chat_history, response_content, model)
    full_response = model_name + ": " + response_content + cost_summary
    
    # Send the final message with the combined response and cost summary
    await cl.Message(
        author="Assistant",
        content=full_response
    ).send()
    
    
@cl.on_chat_resume
async def resume_chat(thread: ThreadDict):
    """
    Resume a previous chat session by reconstructing the conversation history.

    Workflow:
    1. Reinitialize the chat history from the saved thread.
    2. Set up a query engine for document retrieval.
    3. Append previous user and assistant messages to the session.

    Parameters:
    - thread (ThreadDict): A dictionary containing saved chat steps.

    Returns:
    - None: Restores the chat session state.

    Example:
    Resumes a session with prior interactions intact.
    """
    cl.user_session.set("chat_history", [])
    
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=2)
    cl.user_session.set("query_engine", query_engine)
    
    for message in thread["steps"]:
        if message["type"] == "user_message":
            cl.user_session.get("chat_history").append({"role": "user", "content": message["output"]})
        elif message["type"] == "assistant_message":
            cl.user_session.get("chat_history").append({"role": "assistant", "content": message["output"]})