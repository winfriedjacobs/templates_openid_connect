from datetime import UTC, datetime
from typing import Annotated

from authlib.common.security import generate_token
from authlib.integrations.starlette_client import OAuthError
from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse

from src.authentication.oauth import oauth_target, oidc_provider
from src.db.user import internal_users_db
from src.session_state import read_nonce_from_session


DEFAULT_REDIRECT_URL = "/api/protected"

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/login", summary="Initiate OIDC Login")
async def login(
    request: Request,
    target_url: Annotated[str | None, Query(alias="target-url")] = None,
):
    """
    Redirects the user to the OIDC provider (Google, Keycloak) for authentication.
    An optional 'target_url' query parameter can be provided to redirect the user
    to a specific URL after successful authentication.
    """
    # Store the target_url in the session if provided
    if target_url:
        print("target_url", target_url)
        request.session["target_url"] = target_url

    redirect_uri = request.url_for(
        "auth_callback"
    )  # This should match your Authorized redirect URI

    new_nonce = generate_token()
    return await oauth_target.authorize_redirect(
        request, redirect_uri, nonce=new_nonce
    )  # The nonce is used for replay attacks (e.g., to prevent CSRF); Google auth seems to require it.


@router.get("/callback", summary="OIDC Callback Endpoint")
async def auth_callback(request: Request):
    """
    Handles the redirect from the OIDC provider after user authentication.
    Exchanges the authorization code for tokens and establishes a user session.
    """

    # Retrieve the 'state' parameter from the incoming request's query parameters.
    # This state parameter is used to construct the dynamic session key for request.session
    state = request.query_params.get("state")
    if not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication failed: 'state' parameter missing from callback URL.",
        )

    # Retrieve the 'nonce' value from the session
    nonce_from_session = read_nonce_from_session(
        request.session, oidc_provider=oidc_provider, state=state
    )
    if not nonce_from_session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication failed: Nonce not found in session."
            "Session might be invalid, expired, or the state data structure is unexpected.",
        )

    try:
        # Fetch tokens (includes ID Token, Access Token, etc.)
        token = await oauth_target.authorize_access_token(request)

        # At this point, request.session is empty. Presumably because of the call to ...authorize_access_token()
        # That's why we read "nonce" before.

        # Check if 'id_token' exists in the token response
        if "id_token" not in token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authentication failed: 'id_token' missing from Google's response. "
                "Ensure 'openid' scope is requested and Google Cloud Console setup is correct (e.g., APIs enabled, redirect URIs match).",
            )

        # Validate and decode the ID Token (contains user claims)
        # Pass the 'token' dictionary and the retrieved 'nonce'
        user_info = await oauth_target.parse_id_token(
            token=token, nonce=nonce_from_session
        )

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

        # Remove the nonce from the session after successful validation to prevent replay attacks
        # todo request.session.pop(nonce_key, None)

        redirect_url = request.session.get("target_url", DEFAULT_REDIRECT_URL)
        return RedirectResponse(
            url=redirect_url
        )  # Redirect to a protected page or dashboard

    except OAuthError as e:
        # Handle OAuth errors (e.g., user denied access, invalid state)
        print(f"OAuth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {e.description if hasattr(e, 'description') else str(e)}",
        )
    except HTTPException as e:
        # Re-raise the HTTPExceptions that were intentionally raised above
        raise e
    except Exception as e:
        print(
            f"An unexpected error occurred during OIDC callback: {e}"
        )  # Keep this for other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during authentication. Please try again.",
        )


@router.get("/logout", summary="Logout User")
async def logout(request: Request):
    """
    Clears the user's session, effectively logging them out.
    """
    request.session.pop("user", None)
    return {"message": "Logged out successfully"}


__all__ = ["router"]
