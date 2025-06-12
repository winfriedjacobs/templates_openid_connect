from authlib.integrations.starlette_client import OAuth

from src.config import CLIENT_ID, CLIENT_SECRET, KEYCLOAK_BASE_URL, REALM

oauth = OAuth()

keycloak = oauth.register(
    name="keycloak",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"{KEYCLOAK_BASE_URL}/realms/{REALM}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
    # client_kwargs={"scope": "openid email profile groups"},
)

# btw: keycloak == oauth.keycloak
