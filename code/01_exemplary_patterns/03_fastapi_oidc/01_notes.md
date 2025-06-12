#### (1) Start `Keycloak`:
```
docker compose up (--build) keycloak
# or:
podman-compose up (--build) keycloak
```

#### (2) Start `app`:
```
cd app
uv run main.py 
```

#### (3) Run web application:
a. Go to start page

```
http://localhost:9080/
```

b. Login

Click on `login`, then enter credentials:
-  `testuser`/`testpass`

This should the redirect to a (secured) page --> implementation not yet finished


#### (4) Start `nginx`:
- not necessary for this demo
