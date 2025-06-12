# with uv/uvx I would expect it look to like this, but somehow it does not work:
#    uvx uvicorn --factory src:create_app --proxy-headers --host 0.0.0.0 --port 9080 --reload --lifespan on

# So instead, we do not start with uv/uvx, but “classically” with .venv
. .venv/bin/activate

# # DEV
uvicorn --factory src:create_app --proxy-headers --host 0.0.0.0 --port 9080 --reload --lifespan on
return  # stops here!

# # PROD  (beware: we have worker-local variables like 'internal_users_db', here we can expect issues)
uvicorn --factory src:create_app --proxy-headers --host 0.0.0.0 --port 9080 --workers 4 --lifespan on
return  # stops here!
