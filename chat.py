import chainlit as cl
from chainlit.types import ThreadDict

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.core.callbacks import CallbackManager
from llama_index.core import Settings

from utils import count_tokens, trim_chat_history, MAX_TOKEN_LIMIT, MODEL_COSTS, MODEL

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
    Settings.llm = OpenAI(
        model=MODEL, temperature=0.5, max_tokens=1024, streaming=True
    )
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    Settings.context_window = 8192
    Settings.callback_manager = CallbackManager([cl.LlamaIndexCallbackHandler()])
    
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=5)
    cl.user_session.set("query_engine", query_engine)
    
    cl.user_session.set("chat_history", [])

    await cl.Message(
        author="Assistant", content="Hello! Im an AI assistant. You can ask me any question regarding Linux and Git command."
    ).send()
    
    
@cl.on_message
async def response_chat(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")
    msg = cl.Message(content="", author="Assistant")

    chat_history = cl.user_session.get("chat_history")
    chat_history.append({"role": "user", "content": message.content})

    if len(chat_history) == 1: 
        query_input = message.content
    else:
        # Prepare conversation history
        context = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in chat_history])
        query_input = f"Given the following conversation history:\n{context}\nAssistant:"

    # Count tokens
    current_token_count = count_tokens(chat_history)
    print(f"Current token count: {current_token_count}")

    # Trim history if necessary
    if current_token_count > MAX_TOKEN_LIMIT:
        chat_history = trim_chat_history(chat_history)
        print("Chat history trimmed.")

    # Query the model
    res = await cl.make_async(query_engine.query)(query_input)

    # Stream response from the model
    for token in res.response_gen:
        await msg.stream_token(token)
    await msg.send()

    # Add assistant response to chat history
    chat_history.append({"role": "assistant", "content": msg.content})
    
    
@cl.on_chat_resume
async def resume_chat(thread: ThreadDict):
    cl.user_session.set("chat_history", [])
    
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=2)
    cl.user_session.set("query_engine", query_engine)
    
    for message in thread["steps"]:
        if message["type"] == "user_message":
            cl.user_session.get("chat_history").append({"role": "user", "content": message["output"]})
        elif message["type"] == "assistant_message":
            cl.user_session.get("chat_history").append({"role": "assistant", "content": message["output"]})