"""
main.py
=========
The entry point for the chatbot application. It configures the environment, initializes API keys, 
sets up authentication, and starts the chatbot using Chainlit.

Features:
- Loads environment variables for API keys and configuration.
- Initializes OpenAI and Literal API clients.
- Configures user authentication with both password-based and OAuth methods.
- Connects chatbot logic from `chat.py` for message handling and session management.

Dependencies:
- `os`: For accessing environment variables.
- `openai`: For GPT-based model integration.
- `chainlit`: For chatbot session management and user interactions.
- `dotenv`: For loading environment variables from a `.env` file.
- `literalai`: For monitoring OpenAI API usage.

Imported Components:
- `auth_callback` and `oauth_callback` from `auth.py` for authentication.
- `start_chat`, `response_chat`, `resume_chat`, and `choose_profile` from `chat.py` for chatbot logic.
"""

import os
import openai
import chainlit as cl
from dotenv import load_dotenv
from literalai import LiteralClient

from auth import auth_callback, oauth_callback
from chat import start_chat, response_chat, resume_chat, choose_profile

# Load environment variables
load_dotenv()

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Literal API key
literal_api_key = os.getenv("LITERAL_API_KEY")
lai = LiteralClient(api_key=literal_api_key)
lai.instrument_openai()

# Authentication with user/password and oauth 
cl.password_auth_callback(auth_callback)
cl.oauth_callback(oauth_callback)

# Run the chatbot with chainlit
cl.set_chat_profiles(choose_profile)
cl.on_chat_start(start_chat)
cl.on_message(response_chat)
cl.on_chat_resume(resume_chat)