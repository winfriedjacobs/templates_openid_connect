# --- In-memory User Database (Optional: for linking OIDC users to internal profiles) ---
# In a real application, you might want to store more details about users
# after they authenticate via OIDC, linking their 'sub' ID to your internal user ID.
# For simplicity, we'll just check if their OIDC 'sub' is known.

from typing import Dict, Any


internal_users_db: Dict[str, Any] = {}   # Stores {"oidc_sub_id": {"username": "...", "roles": [...]}}


__all__ = ["internal_users_db"]
