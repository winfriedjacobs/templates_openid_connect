## OpenID Connect Authentication in a FastAPI App

- FastAPI
- authlib
- Google authentication (version 1)
- Keycloak authentication (version 2)

Based on a guide from Google Gemini AI 
- see https://g.co/gemini/share/12a364bcc660
- and local files "GEMINI_AI_GUIDE.md" und "GEMINI_AI_GUIDE_CODE.md"


### Pycharm
Always open Pycharm in/from the ./app directory, then it finds the correct import/package hierarchy.

### Start the application it with one of these script files:

***Prerequisite for each alternative***: installation with "uv" ("uv sync" etc)


Alternative A: run with "uv"
```
uv run start_uvicorn.py
```

Alternative B: Docker based
(work in progress)
- development locally with Docker + uv
- expected result #1: a Docker container that can be deployed for production / staging (in a CI/CD pipeline)
  -> see `uv-docker-example` and corresponding documentation in the uv documentation
- expected result #2: a Docker container that can be used for development 
  (so that everything is installed in the container, if this makes even sense)
  -> see `uv-docker-example` and corresponding documentation in the uv documentation
- expected result #3: a Docker container that can be used for development with Pycharm
  -> see the respective documentation for PyCharm
  



Alternative C: conventional start
```
# cd ./app
. start_uvicorn_classic.sh
```
*Note:* `start_uvicorn_classic.sh` does NOT use uv/uvx, but activates its .venv environment.
The .env environment exists when installing everything with "uv" (see above).
