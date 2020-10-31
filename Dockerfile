# Dockerfile
# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
FROM python:3-alpine
# Set an environment variable with the directory
# where we'll be running the app
ENV APP="/app" \
    PYTHONPATH="/usr/lib/python3.8/site-packages"

# We copy the codebase into the image
COPY app $APP

# Run APK to update packages, upgrade packages, and add curl.
# PIP is then upgraded. Switch to app directory and install our
# python dependencies via setuptools and pip.
RUN apk update; \
    apk upgrade; \
    apk add curl; \
    /usr/local/bin/python -m pip install --upgrade pip; \
    cd ${APP} ; \
    pip install .; \
    chmod u+x /app/start.sh;

WORKDIR $APP
ENTRYPOINT ["/app/start.sh"]
