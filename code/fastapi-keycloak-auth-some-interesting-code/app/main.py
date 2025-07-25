from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from auth import keycloak
from session import set_session, clear_session, get_session
from deps import require_group, require_role

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("<a href='/login'>Login</a>")

@app.get("/login")
async def login(request: Request):
    return await keycloak.authorize_redirect(request, redirect_uri="http://localhost:8000/callback")

@app.get("/callback")
async def callback(request: Request):
    token = await keycloak.authorize_access_token(request)
    user = await keycloak.parse_id_token(request, token)
    response = RedirectResponse(url="/protected")
    set_session(response, user)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    clear_session(response)
    return response

@app.get("/protected")
def protected(user=Depends(require_group("/AppAdmins"))):
    return {"message": f"Hello, {user['preferred_username']} (Group: AppAdmins)"}

@app.get("/admin")
def admin_only(user=Depends(require_role("admin"))):
    return {"message": f"Hello Admin {user['preferred_username']}"}
