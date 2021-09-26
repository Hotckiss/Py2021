import os

def get_toloka_token():
    return os.environ.get("TOLOKA_TOKEN")