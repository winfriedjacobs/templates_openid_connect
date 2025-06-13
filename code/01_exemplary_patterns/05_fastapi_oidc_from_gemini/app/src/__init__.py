"""
We use this script only or starting with uvicorn, see start_uvicorn_classic.sh

"""

from src.create_app import create_app


__all__ = ["create_app"]  # to make the linter happy
