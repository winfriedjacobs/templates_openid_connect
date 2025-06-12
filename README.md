This repository contains all the code from `76_oidc_auth`
- rsynced from there to `./code`
- but without their `.git` , `.ven` , and `__pycache__` files

It provides 2 templates for creating 'authenticated' applications:

1. based on `OpenID Connect` and (the API Gateway) `APISIX`
- with APISIX, Keycloak and a mockup micro service
- APISIX implements the OIDC login workflow, and the access control for some endpoints 

2. based on `OpenID Connect` and a `FastAPI` microservice
   - the `FastAPI` microservice implements the OIDC login workflow (based on the authlib library);
     it implements access control for some endpoints

   - the working template is in ./01..../05...Gemini..., because only Gemini could provide an almost working basis for the implementation

