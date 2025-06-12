"""
Initialize Authlib OAuth client
"""

from authlib.integrations.starlette_client import OAuth

from config.oidc import (
    GOOGLE_OIDC_PROVIDER,
    KEYCLOAK_OIDC_PROVIDER,
    google_oidc_config,
    keycloak_oidc_config,
)

_oauth = OAuth()

# we can register more than one authentication instance (but we use only one of them in this demo application
_oauth_google = (  # we use _oauth_google.(...) instead of _oauth.google.(...)
    _oauth.register(
        name=google_oidc_config.NAME,
        client_id=google_oidc_config.CLIENT_ID,
        client_secret=google_oidc_config.CLIENT_SECRET,
        server_metadata_url=google_oidc_config.SERVER_METADATA_URL,
        client_kwargs={
            "scope": google_oidc_config.SCOPE
        },  # Scopes requested from Google
    )
)
_oauth_keycloak = (  # we use _oauth_keycloak.(...) instead of _oauth.keycloak.(...)
    _oauth.register(
        name=keycloak_oidc_config.NAME,
        client_id=keycloak_oidc_config.CLIENT_ID,
        client_secret=keycloak_oidc_config.CLIENT_SECRET,
        server_metadata_url=keycloak_oidc_config.SERVER_METADATA_URL,
        client_kwargs={"scope": keycloak_oidc_config.SCOPE},
    )
)

# We use one of the providers, for testing purposes we can initialize both Google and Keycloak
# We could even use both at the same time, which we don't; but at startup we decide which one to use


oidc_provider = GOOGLE_OIDC_PROVIDER
if oidc_provider == GOOGLE_OIDC_PROVIDER:
    oauth_target = (
        _oauth_google  # or _oauth.google, but _oauth_google is stable when refactoring
    )
elif oidc_provider == KEYCLOAK_OIDC_PROVIDER:
    oauth_target = _oauth_keycloak  # or _oauth.keycloak, but _oauth_keycloak is stable when refactoring
else:
    raise Exception("Invalid OIDC provider specified.")


__all__ = ["oidc_provider", "oauth_target"]
