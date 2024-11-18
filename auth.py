"""
auth.py
=========
Handles user authentication for the chatbot application.

Features:
- Password-based authentication with predefined user credentials.
- OAuth-based authentication for third-party providers.

Dependencies:
- Chainlit: Used for authentication callback functions.
"""

import chainlit as cl
from typing import Optional, Dict

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """
    Authenticate users based on username and password.

    Parameters:
    - username (str): The user's username.
    - password (str): The user's password.

    Returns:
    - cl.User: An authenticated user object with metadata if credentials are valid.
        - identifier (str): Unique identifier for the user.
        - metadata (dict): Additional information about the user:
            - role: Specifies the user's role (e.g., "admin" or "user").
            - provider: Indicates the authentication method (e.g., "credentials").
    - None: If the provided username and password are invalid.
    
    Predefined Credentials:
    - Admin: username="admin", password="admin"
    - Regular User: username="taikhoan916", password="matkhau916"

    Example:
    >>> auth_callback("admin", "admin")
    User(identifier="admin", metadata={"role": "admin", "provider": "credentials"})
    >>> auth_callback("invalid_user", "wrong_password")
    None
    """
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
def oauth_callback(
    provider_id: str, 
    token: str, 
    raw_user_data: Dict[str, str], 
    default_user: cl.User
) -> Optional[cl.User]:
    """
    Handle OAuth-based authentication for third-party providers.

    Parameters:
    - provider_id (str): Identifier for the OAuth provider (e.g., "github", "gitlab").
    - token (str): The token issued by the OAuth provider after successful authentication.
    - raw_user_data (dict): User data returned by the OAuth provider.
        Example:
        {
            "id": "12345",
            "email": "user@example.com",
            "name": "John Doe"
        }
    - default_user (cl.User): A default user object provided by the application.

    Returns:
    - cl.User: The default user object to represent the authenticated user.
    
    Note:
    - This implementation currently does not validate the token or process raw_user_data.
      For production, consider adding token validation and mapping user data to your system.

    Example:
    >>> oauth_callback("github", "some_token", {"id": "123", "email": "user@example.com"}, default_user)
    default_user
    """
    return default_user