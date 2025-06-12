from itsdangerous import URLSafeSerializer
from fastapi import Request, Response
from config import SECRET_KEY

serializer = URLSafeSerializer(SECRET_KEY)
COOKIE_NAME = "session"

def set_session(response: Response, user: dict):
    session = serializer.dumps(user)
    response.set_cookie(COOKIE_NAME, session, httponly=True)

def get_session(request: Request):
    cookie = request.cookies.get(COOKIE_NAME)
    if not cookie:
        return None
    try:
        return serializer.loads(cookie)
    except Exception:
        return None

def clear_session(response: Response):
    response.delete_cookie(COOKIE_NAME)

def user_in_group(user: dict, group: str) -> bool:
    return group in user.get("groups", [])

def user_has_role(user: dict, role: str) -> bool:
    return role in user.get("realm_access", {}).get("roles", [])
