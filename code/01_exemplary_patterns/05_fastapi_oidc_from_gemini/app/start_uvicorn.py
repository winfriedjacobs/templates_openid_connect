"""
2 use cases:

1. Start it in the IDE (which was set up as a .venv project)
2. Start it in the terminal with UV: `uv run start_uvicorn.py`

"""

import uvicorn

START_APP_AS_OBJECT = True


def start_app_as_object():
    # alternative 1:
    # we pass an FastAPI object to uvicorn.run;
    # in this case the params "reload=True" and "workers=4" do NOT work

    from src.create_app import create_app

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=9080)


def start_app_as_string():
    # alternative 2:
    # here we can pass "reload=True" or "workers=4" (not necessary in the IDE)
    uvicorn.run(
        "src:create_app",
        factory=True,
        proxy_headers=True,
        host="0.0.0.0",
        port=9080,
        reload=True,
        lifespan="on",
    )


if __name__ == "__main__":
    if START_APP_AS_OBJECT:
        start_app_as_object()
    else:
        start_app_as_string()
