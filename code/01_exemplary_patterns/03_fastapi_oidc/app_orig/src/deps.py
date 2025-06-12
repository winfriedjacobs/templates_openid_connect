from fastapi import HTTPException, Request

from src.session import get_session, user_has_role, user_in_group


def require_group(group: str):
    def dependency(request: Request):
        user = get_session(request)
        if not user or not user_in_group(user, group):
            raise HTTPException(status_code=403, detail=f"Must be in group {group}")
        return user

    return dependency


def require_role(role: str):
    def dependency(request: Request):
        user = get_session(request)
        if not user or not user_has_role(user, role):
            raise HTTPException(status_code=403, detail=f"Must have role {role}")
        return user

    return dependency
