from authlib.integrations.starlette_client import OAuth

from src.config.oidc import oidc_config


def create_oauth_keycloak():
    # oauth = OAuth(config)  ???
    oauth = OAuth()

    return oauth.register(
        name="keycloak",
        client_id=oidc_config.CLIENT_ID,
        client_secret=oidc_config.CLIENT_SECRET,
        server_metadata_url=oidc_config.OIDC_CONF_URL,
        client_kwargs={"scope": "openid email profile"},
    )
