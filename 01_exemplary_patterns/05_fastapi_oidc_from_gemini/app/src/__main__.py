"""
This modul starts the uvicorn ASGI server with the `app` object from main (without the need to explicitly import it).

Code started with Gemini: https://gemini.google.com/app/2530e9b2cbbd2bf1?hl=de

The app is started by doing this in the terminal:
```
( cd ./app )
uv run src
```
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "create_app:create_app", factory=True, host="0.0.0.0", port=9080, reload=True
    )  # workers=4 --> only when reload=False
    # can be run like this:
    #     from create_app import create_app
    #     app = create_app()
    #     uvicorn.run(app, host="0.0.0.0", port=9080)
    # but in this case not with params "reload=True" and "workers=4" (and maybe also not with debug=True)
