from secrets import token_urlsafe

#
WEB_SESSION_SECRET_KEY = token_urlsafe(64)


__all__ = ["WEB_SESSION_SECRET_KEY"]
