from authlib.integrations.starlette_client import OAuth
from config import *

oauth = OAuth()

keycloak = oauth.register(
    name='keycloak',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"{KEYCLOAK_BASE_URL}/realms/{REALM}/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid email profile groups'},
)
