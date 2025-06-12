import os

APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:9080")

print("APP_BASE_URL", APP_BASE_URL)

KEYCLOAK_BASE_URL = os.getenv("KEYCLOAK_BASE_URL", "http://localhost:8080")
REALM = os.getenv("KEYCLOAK_REALM", "demo")
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "apisix-client")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "LJbGDn2QCj9RT9hWy77XKvyB8I3FP4FX")
# Todo delete: SECRET_KEY = os.getenv("APP_SECRET_KEY", "super-secret-key")

# REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/callback")
REDIRECT_URI = f"{APP_BASE_URL}/callback"
