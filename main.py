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






