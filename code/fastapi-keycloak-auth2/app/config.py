import os

KEYCLOAK_BASE_URL = os.getenv("KEYCLOAK_BASE_URL", "http://localhost:8080")
REALM = os.getenv("KEYCLOAK_REALM", "myrealm")
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "myclient")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "mysecret")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/callback")
SECRET_KEY = os.getenv("APP_SECRET_KEY", "super-secret-key")
