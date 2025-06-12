## Which part of the program is supposed to store the nonce in the session?

The nonce is stored in the session by Authlib itself, specifically within the oauth.google.authorize_redirect(request, redirect_uri) call.
When you navigate to the /login endpoint and this line is executed:
Python
return await oauth.google.authorize_redirect(request, redirect_uri)

Authlib performs several actions internally:
It generates a unique nonce value.
It stores this nonce value in your application's session, which is managed by the SessionMiddleware. The key used for storing the nonce is typically _authlib_nonce_{provider_name}, so in your case, _authlib_nonce_google.
It constructs the authorization URL for Google, including the generated nonce as a parameter.
It then redirects the user's browser to this Google authorization URL.
This ensures that when Google redirects back to your /auth/callback endpoint with the id_token, your application can retrieve the stored nonce from the session and verify that it matches the nonce claim in the id_token. This process is critical for preventing replay attacks.
The fact that request.session.get(nonce_key) returns None indicates an issue with the session persistence itself between the /login redirect and the /auth/callback endpoint. This is why I've been focusing on potential APP_SECRET_KEY issues or browser cookie problems.

