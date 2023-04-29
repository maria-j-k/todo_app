# todo_app

ToDo application created with FastAPI and MongoDB.
https://coral-app-rmdjl.ondigitalocean.app


NOTES:

Password reset functionality is not yet implemented on production.

To use social auth (Google login) you need to go to the endpoint directly in your browser (no support for
OpenAPI yet)

On the root of the application you'll find the links for social auth and different versions of the documentation.

Users authenticated only with their Google account need to use reset password functionality
if they want to log in directly with their credentials. `reset_request` endpoint sends a link on an email
address provided in the request body a link, on which a `post` request should be sent with the new
password in the body.


## Setup

### Locally
1. clone the repository
2. set `poetry.virutalenvscreate` to false
3. create virtual environment using Python 3.9.10 and activate it
4. run `poetry install`
5. get your Google client secret and client ID to enable Google login
6. set up your environmental variables in `.env-sample` and rename it to `.env`
7. in the top level directory create the `credentials.json` to enable
mailing functionality (needed for password reset)
8. run `uvicor app.main:app --reload`

### In the Docker container

1. clone the repository
2. set up your environmental variables in `.env-sample` and rename it to `.env`
3. get your Google client secret and client ID to enable Google login
4. in the top level directory create the `credentials.json` to enable
mailing functionality (needed for password reset)
5. run `docker-compose up --build`


## Features to implement

1. Enable the use of Google login in Swagger
2. Enable email sending on production
3. Add superuser and the admins views
4. Add logging
