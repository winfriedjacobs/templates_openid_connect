I'll create a Python FastAPI application with login and authentication using Authlib for OAuth 2.0. This example will include user registration, login, and protected endpoints using JWT tokens.

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.integrations.starlette_client import OAuth
from authlib.jose import jwt
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime, timedelta
from starlette.config import Config
from starlette.requests import Request

app = FastAPI()

# Configuration
config = Config('.env')  # Assuming .env file for sensitive data
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth setup
oauth = OAuth(config)
oauth.register(
    name='example',
    client_id='your-client-id',
    client_secret='your-client-secret',
    authorize_url='https://example.com/oauth/authorize',
    token_url='https://example.com/oauth/token',
    userinfo_endpoint='https://example.com/oauth/userinfo'
)

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
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
    authorizationUrl="https://example.com/oauth/authorize",
    tokenUrl="https://example.com/oauth/token",
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
                detail="Invalid authentication credentials"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return email

# Routes
@app.post("/register", response_model=Token)
async def register(user: User):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                 (user.email, user.password))  # In production, hash the password
        conn.commit()
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    finally:
        conn.close()

@app.post("/login", response_model=Token)
async def login(user: User):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT email, password FROM users WHERE email = ?", (user.email,))
    db_user = c.fetchone()
    conn.close()
    
    if not db_user or db_user[1] != user.password:  # In production, verify hashed password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/oauth/login")
async def oauth_login(request: Request):
    redirect_uri = "http://localhost:8000/oauth/callback"
    return await oauth.example.authorize_redirect(request, redirect_uri)

@app.get("/oauth/callback")
async def oauth_callback(request: Request):
    token = await oauth.example.authorize_access_token(request)
    user = await oauth.example.get(token['userinfo_endpoint']).json()
    
    # Store user in database or update existing
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (email, password) VALUES (?, ?)",
             (user['email'], 'oauth_' + user['sub']))
    conn.commit()
    conn.close()
    
    access_token = create_access_token(data={"sub": user['email']})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! This is a protected endpoint."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

To run this FastAPI application, you'll need to:

1. Install dependencies:
```bash
pip install fastapi uvicorn authlib python-jose[cryptography] pydantic sqlite3
```

2. Create a `.env` file with OAuth provider credentials:
```
EXAMPLE_CLIENT_ID=your-client-id
EXAMPLE_CLIENT_SECRET=your-client-secret
```

3. Notes:
- This example uses SQLite for simplicity. In production, use a proper database and hash passwords.
- Replace the OAuth provider URLs with your actual provider's endpoints (e.g., Google, GitHub).
- The SECRET_KEY should be stored securely in environment variables.
- The OAuth example uses a generic provider; configure it for your specific OAuth provider.
- Run the app with: `uvicorn main:app --reload`

Endpoints:
- POST `/register`: Create a new user
- POST `/login`: Login with email/password
- GET `/oauth/login`: Start OAuth flow
- GET `/oauth/callback`: Handle OAuth callback
- GET `/protected`: Access protected resource with JWT token

This implementation provides basic authentication with both traditional email/password and OAuth 2.0 flows, using JWT for token-based authentication.
