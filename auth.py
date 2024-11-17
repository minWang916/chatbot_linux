import chainlit as cl
from typing import Optional, Dict

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    elif (username, password) == ("taikhoan916", "matkhau916"):
        return cl.User(
            identifier="taikhoan916", metadata={"role": "user", "provider": "credentials"}
        )
    else:
        return None
    
@cl.oauth_callback
def oauth_callback(provider_id: str,token: str,raw_user_data: Dict[str, str],default_user: cl.User,) -> Optional[cl.User]:
  return default_user
