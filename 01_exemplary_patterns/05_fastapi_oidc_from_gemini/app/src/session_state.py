from typing import Any, Dict, Optional


def read_nonce_from_session(
    session: Dict[str, Any], *, oidc_provider: str, state: str
) -> Optional[str]:
    """
    Read the nonce from the session.
    """

    # todo: comment ???
    # Construct the dynamic session key where Authlib stores the state data (including nonce).
    # Based on your session content, it's "_state_{provider_name}_{state_value}"
    session_state_key = f"_state_{oidc_provider}_{state}"

    return session.get(session_state_key, {}).get("data", {}).get("nonce")
