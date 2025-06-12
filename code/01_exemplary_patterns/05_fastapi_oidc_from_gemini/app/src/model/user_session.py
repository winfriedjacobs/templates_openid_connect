from typing import Optional

from pydantic import BaseModel


class UserSession(BaseModel):
    """Model for user information stored in the session."""

    id: str  # OIDC subject ID (unique identifier from IdP)
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None  # URL to user's profile picture
