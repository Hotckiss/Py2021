FROM python:3.8

RUN python3.8 -m pip install Flask
RUN python3.8 -m pip install Flask-Pydantic
RUN python3.8 -m pip install pydantic

WORKDIR /workspace

COPY FlaskApp /workspace

ENTRYPOINT python3.8 /workspace/app.py --port 6067 --host ::
