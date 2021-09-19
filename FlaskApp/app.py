import uuid

from argparse import ArgumentParser
from flask import Flask
from flask_pydantic import validate
from pydantic import BaseModel

app = Flask(__name__)


class Track(BaseModel):
    name: str
    max_parallel_pools: int
    min_pool_acceptance_rate: float
    max_hourly_appeals: int
    check_interval_minutes: int
    soft_alert_multiplier: float


class TrackResponse(BaseModel):
    id: str
    message: str


class TrackInfoResponse(BaseModel):
    track_id: str
    track: Track


class InMemTrackStorage:
    def __init__(self):
        self.mem = {}

    def insert(self, track: Track) -> str:
        tid = str(uuid.uuid4())
        self.mem[tid] = track

        return tid

    def get(self, tid: str) -> Track:
        result = self.mem.get(tid)
        if result is None:
            raise ValueError("Requested track not found!")

        return result


storage = InMemTrackStorage()


@app.route('/api/track', methods=['POST'])
@validate()
def register_track(body: Track):
    if body.max_hourly_appeals < 0:
        return {'error': 'Appeals count can not be negative'}, 400

    if (body.min_pool_acceptance_rate < 0) or (body.min_pool_acceptance_rate > 1):
        return {'error': 'Pool AC rate must be between 0 and 1'}, 400

    if body.max_parallel_pools < 0:
        return {'error': 'Pools count can not be negative'}, 400

    if body.check_interval_minutes < 0:
        return {'error': 'Check interval can not be negative'}, 400

    if body.soft_alert_multiplier <= 0:
        return {'error': 'Check interval must be positive'}, 400

    soft_pool_ac_rate = body.min_pool_acceptance_rate * body.soft_alert_multiplier
    soft_appeals_count = int(body.max_hourly_appeals * body.soft_alert_multiplier)

    track_id = storage.insert(body)
    response_message = f'Registered track with id={track_id} and soft thresholds {soft_pool_ac_rate} for pools and ' \
                       f'{soft_appeals_count} for appeals! '

    return TrackResponse(id=track_id, message=response_message)


@app.route('/api/track/<track_id>', methods=['GET'])
@validate()
def track_info(track_id: str):
    try:
        track = storage.get(track_id)
    except ValueError:
        return {'error': f'Track with id={track_id} not found!'}, 400
    except Exception:
        return {'error': f'Failed to retrieve track with id={track_id}, internal error!'}, 500
    return TrackInfoResponse(track_id=track_id, track=track)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
