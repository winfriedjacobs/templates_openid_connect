from src.create_app import create_app

if __name__ == "__main__":
    import uvicorn

    app = create_app()

    uvicorn.run(app, host="localhost", port=9080)


# # alternatively:
#
# async def main():
#     app = create_app()
#
#     config = uvicorn.Config(app, port=9080, log_level="info")
#     server = uvicorn.Server(config)
#     await server.serve()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
