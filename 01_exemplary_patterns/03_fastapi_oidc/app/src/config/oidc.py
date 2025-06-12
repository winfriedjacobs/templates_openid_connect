from dataclasses import dataclass

from .basic import basic_config


@dataclass(frozen=True)
class OidcConfig:
    CLIENT_ID: str
    CLIENT_SECRET: str
    KEYCLOAK_BASE_URL: str
    KEYCLOAK_REALM: str

    @property
    def OIDC_CONF_URL(self):
        return f"""{self.KEYCLOAK_BASE_URL}/realms/{self.KEYCLOAK_REALM}/.well-known/openid-configuration"""


oidc_config = OidcConfig(
    CLIENT_ID=basic_config("CLIENT_ID"),  # "apisix-client",
    CLIENT_SECRET=basic_config("CLIENT_SECRET"),  # "IKxIZ2sfpC8jcLom7FNKGEXGcrtgN5RZ"
    KEYCLOAK_BASE_URL=basic_config("KEYCLOAK_BASE_URL"),  # "http://localhost:8080"
    KEYCLOAK_REALM=basic_config("KEYCLOAK_REALM"),  # "demo"
)

__all__ = ["oidc_config"]
