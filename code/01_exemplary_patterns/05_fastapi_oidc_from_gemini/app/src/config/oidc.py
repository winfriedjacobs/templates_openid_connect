from dataclasses import dataclass

# from .basic import basic_config


GOOGLE_OIDC_PROVIDER = "google"
KEYCLOAK_OIDC_PROVIDER = "keycloak"


@dataclass(frozen=True)
class OidcConfig:

    NAME: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    SERVER_METADATA_URL: str
    SCOPE: str = "openid email profile"

    # from a previous implementation, todo: obsolete
    # @property
    # def OIDC_CONF_URL(self):
    #     return f"""{self.KEYCLOAK_BASE_URL}/realms/{self.KEYCLOAK_REALM}/.well-known/openid-configuration"""


# ---

# comments from Gemeini:

# OAuth2 / OpenID Connect Provider details (e.g., Google)
# You need to create an OAuth 2.0 Client ID in the Google Cloud Console
# and enable the Google+ API (or Google People API for newer applications).
# Set Authorized JavaScript origins to http://localhost:8000
# Set Authorized redirect URIs to http://localhost:8000/auth/callback

google_oidc_config = OidcConfig(
    NAME=GOOGLE_OIDC_PROVIDER,
    CLIENT_ID="1074698109380-kbafcgqtile117l08sr6tncih9j18ocp.apps.googleusercontent.com",
    CLIENT_SECRET="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",
    SERVER_METADATA_URL="https://accounts.google.com/.well-known/openid-configuration",
)

# ---

KEYCLOAK_BASE_URL = "http://localhost:8080"
KEYCLOAK_REALM = "demo"
keycloak_oidc_config = OidcConfig(
    NAME=KEYCLOAK_OIDC_PROVIDER,
    CLIENT_ID="apisix-client",
    CLIENT_SECRET="sgxijWlwLh0K8qmmBNmWhrdokrCGQpiZ",
    SERVER_METADATA_URL=f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM}/.well-known/openid-configuration",
)


__all__ = [
    "OidcConfig",
    "google_oidc_config",
    "keycloak_oidc_config",
    "GOOGLE_OIDC_PROVIDER",
    "KEYCLOAK_OIDC_PROVIDER",
]
