"""
started with Gemini: https://gemini.google.com/app/2530e9b2cbbd2bf1?hl=de
"""

from datetime import UTC, datetime
from typing import Optional

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

# --- Configuration ---
# IMPORTANT: Replace with your actual secrets and configuration!
# For production, use environment variables for these secrets.
# export APP_SECRET_KEY="a_long_random_string_for_session_middleware"
# export GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
# export GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"

# Your application's secret key for session management (MUST BE LONG AND RANDOM)
APP_SECRET_KEY = (
    "your-app-secret-key-for-session-middleware-change-this-in-production-!!!!!!"
)

# OAuth2 / OpenID Connect Provider details (e.g., Google)
# You need to create an OAuth 2.0 Client ID in the Google Cloud Console
# and enable the Google+ API (or Google People API for newer applications).
# Set Authorized JavaScript origins to http://localhost:8000
# Set Authorized redirect URIs to http://localhost:8000/auth/callback
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"  # <<< REPLACE THIS
GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"  # <<< REPLACE THIS

# FastAPI app initialization
app = FastAPI(title="FastAPI Authlib OpenID Connect Demo")

# Add SessionMiddleware to handle sessions (required for Authlib's client)
app.add_middleware(SessionMiddleware, secret_key=APP_SECRET_KEY)

# Initialize Authlib OAuth client
oauth = OAuth()
oauth.register(
    name="google",  # The name of your OIDC provider
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},  # Scopes requested from Google
)


# --- Pydantic Models ---
class UserSession(BaseModel):
    """Model for user information stored in the session."""

    id: str  # OIDC subject ID (unique identifier from IdP)
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None  # URL to user's profile picture


# --- In-memory User Database (Optional: for linking OIDC users to internal profiles) ---
# In a real application, you might want to store more details about users
# after they authenticate via OIDC, linking their 'sub' ID to your internal user ID.
# For simplicity, we'll just check if their OIDC 'sub' is known.
internal_users_db = {}  # Stores {"oidc_sub_id": {"username": "...", "roles": [...]}}


# --- Authentication Dependency ---


async def get_current_user_from_session(request: Request) -> Optional[UserSession]:
    """
    Dependency to get the current authenticated user from the session.
    """
    user_info = request.session.get("user")
    if user_info:
        return UserSession(**user_info)
    return None


def require_auth(current_user: UserSession = Depends(get_current_user_from_session)):
    """
    Dependency to enforce authentication. If no user is in session, raises 401.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in.",
            headers={
                "WWW-Authenticate": "Bearer"
            },  # Still good practice for API clients
        )
    return current_user


# --- API Endpoints ---


@app.get("/login", summary="Initiate OIDC Login")
async def login(request: Request):
    """
    Redirects the user to the OIDC provider (Google) for authentication.
    """
    redirect_uri = request.url_for(
        "auth_callback"
    )  # This should match your Authorized redirect URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback", summary="OIDC Callback Endpoint")
async def auth_callback(request: Request):
    """
    Handles the redirect from the OIDC provider after user authentication.
    Exchanges the authorization code for tokens and establishes a user session.
    """
    try:
        # Fetch tokens (includes ID Token, Access Token, etc.)
        token = await oauth.google.authorize_access_token(request)

        # Validate and decode the ID Token (contains user claims)
        # Authlib automatically validates the ID Token for signature, expiry, audience, etc.
        user_info = await oauth.google.parse_id_token(request, token)

        # Store essential user information in the session
        # Ensure only serializable data is stored in the session
        request.session["user"] = {
            "id": user_info.get(
                "sub"
            ),  # 'sub' is the unique identifier for the user from the IdP
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
        }

        # Optionally, check if this user (identified by 'sub') exists in your internal DB
        # If not, you might want to create a new internal user profile here
        oidc_sub_id = user_info.get("sub")
        if oidc_sub_id and oidc_sub_id not in internal_users_db:
            print(
                f"New OIDC user '{user_info.get('name')}' (sub: {oidc_sub_id}) logged in. Creating internal profile if needed."
            )
            internal_users_db[oidc_sub_id] = {
                "username": user_info.get("name", oidc_sub_id),
                "created_at": datetime.now(UTC).isoformat(),
            }

        return RedirectResponse(
            url="/protected"
        )  # Redirect to a protected page or dashboard

    except OAuthError as e:
        # Handle OAuth errors (e.g., user denied access, invalid state)
        print(f"OAuth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {e.description if hasattr(e, 'description') else str(e)}",
        )
    except Exception as e:
        print(f"Unexpected error during OIDC callback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during authentication.",
        )


@app.get("/logout", summary="Logout User")
async def logout(request: Request):
    """
    Clears the user's session, effectively logging them out.
    """
    request.session.pop("user", None)
    return {"message": "Logged out successfully"}


@app.get(
    "/protected", summary="Access a protected resource (requires OIDC authentication)"
)
async def read_protected_resource(current_user: UserSession = Depends(require_auth)):
    """
    An example endpoint that requires a valid OIDC authentication session.
    """
    return {
        "message": f"Hello {current_user.name or current_user.email or current_user.id}! You accessed a protected resource.",
        "user_info": current_user.dict(),
    }


@app.get("/me", summary="Get current user info (if authenticated)")
async def get_my_info(
    current_user: Optional[UserSession] = Depends(get_current_user_from_session),
):
    """
    Returns information about the current user if authenticated, otherwise returns None.
    """
    if current_user:
        return {"authenticated": True, "user": current_user.dict()}
    return {"authenticated": False, "user": None}


@app.get("/", summary="Root endpoint")
async def read_root():
    """
    Basic root endpoint.
    """
    return {
        "message": "Welcome to the FastAPI Authlib OpenID Connect Demo! Go to /login to authenticate."
    }
