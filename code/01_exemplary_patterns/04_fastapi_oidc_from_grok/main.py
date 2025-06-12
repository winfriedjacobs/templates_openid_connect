import sqlite3
from datetime import datetime, timedelta
from secrets import token_urlsafe

from authlib.integrations.starlette_client import OAuth
from authlib.jose import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request


CLIENT_ID = "apisix-client"
CLIENT_SECRET = "IKxIZ2sfpC8jcLom7FNKGEXGcrtgN5RZ"
KEYCLOAK_BASE_URL = "http://localhost:8080"
KEYCLOAK_REALM = "demo"
# XXX = f"{KEYCLOAK_BASE_URL}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
AUTHORIZE_URL = "http://localhost:9080/oauth/authorize"
TOKEN_URL = "http://localhost:9080/oauth/token"
USERINFO_URL = "http://localhost:9080/oauth/userinfo"


app = FastAPI()

# Configuration
config = Config(".env")  # Assuming .env file for sensitive data
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Add SessionMiddleware to FastAPI
SESSION_SECRET_KEY = token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# OAuth setup
oauth = OAuth(config)
oauth.register(
    name="keycloak",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_url=AUTHORIZE_URL,
    token_url=TOKEN_URL,
    userinfo_endpoint=USERINFO_URL,
    # authorize_url="https://4.com/oauth/authorize",
    # token_url="https://example.com/oauth/token",
    # userinfo_endpoint="https://example.com/oauth/userinfo",
)


# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        """
CREATE TABLE IF NOT EXISTS users
(id INTEGER PRIMARY KEY AUTOINCREMENT,
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL)
    """
    )
    conn.commit()
    conn.close()


init_db()


# Pydantic models
class User(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# OAuth2 scheme
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZE_URL,
    tokenUrl=TOKEN_URL,
    # authorizationUrl="https://example.com/oauth/authorize",
    # tokenUrl="https://example.com/oauth/token",
)


# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode({"alg": ALGORITHM}, to_encode, SECRET_KEY)
    return encoded_jwt.decode()


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return email


# Routes
@app.post("/register", response_model=Token)
async def register(user: User):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (user.email, user.password),
        )  # In production, hash the password
        conn.commit()
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    finally:
        conn.close()


@app.post("/login", response_model=Token)
async def login(user: User):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT email, password FROM users WHERE email = ?", (user.email,))
    db_user = c.fetchone()
    conn.close()

    if (
        not db_user or db_user[1] != user.password
    ):  # In production, verify hashed password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/oauth/login")
async def oauth_login(request: Request):
    redirect_uri = request.url_for("/oauth/callback")
    return await oauth.keycloak.authorize_redirect(request, redirect_uri)


@app.get("/oauth/callback")
async def oauth_callback(request: Request):
    token = await oauth.keycloak.authorize_access_token(request)
    user = await oauth.keycloak.get(token["userinfo_endpoint"]).json()

    # Store user in database or update existing
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO users (email, password) VALUES (?, ?)",
        (user["email"], "oauth_" + user["sub"]),
    )
    conn.commit()
    conn.close()

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! This is a protected endpoint."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9080)
