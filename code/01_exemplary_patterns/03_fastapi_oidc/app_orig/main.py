import asyncio

import uvicorn

from src.main import create_app


async def main():
    app = create_app()

    config = uvicorn.Config(app, port=9080, log_level="info")
    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
