import uuid

from argparse import ArgumentParser
from flask import Flask
from flask_pydantic import validate
from pydantic import BaseModel

from lib.api import validate_track, register, info
from lib.models import Track, TrackResponse, TrackInfoResponse
from lib.storage import storage

app = Flask(__name__)


@app.route('/api/track', methods=['POST'])
@validate()
def register_track(body: Track):
    return register(body)


@app.route('/api/track/<track_id>', methods=['GET'])
@validate()
def track_info(track_id: str):
    return info(track_id)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
