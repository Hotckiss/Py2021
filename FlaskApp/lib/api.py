from lib.models import Track, TrackResponse, TrackInfoResponse
from lib.storage import storage


def validate_track(body: Track):
    if body.max_hourly_appeals < 0:
        return False, {'error': 'Appeals count can not be negative'}, 400

    if (body.min_pool_acceptance_rate < 0) or (body.min_pool_acceptance_rate > 1):
        return False, {'error': 'Pool AC rate must be between 0 and 1'}, 400

    if body.max_parallel_pools < 0:
        return False, {'error': 'Pools count can not be negative'}, 400

    if body.check_interval_minutes < 0:
        return False, {'error': 'Check interval can not be negative'}, 400

    if body.soft_alert_multiplier <= 0:
        return False, {'error': 'Check interval must be positive'}, 400

    return True, None, None


def register(body: Track):
    status, resp, code = validate_track(body)

    if not status:
        return resp, code

    soft_pool_ac_rate = body.min_pool_acceptance_rate * body.soft_alert_multiplier
    soft_appeals_count = int(body.max_hourly_appeals * body.soft_alert_multiplier)

    track_id = storage.insert(body)
    response_message = f'Registered track with id={track_id} and soft thresholds {soft_pool_ac_rate} for pools and ' \
                       f'{soft_appeals_count} for appeals! '

    return TrackResponse(id=track_id, message=response_message)


def info(track_id: str):
    try:
        track = storage.get(track_id)
    except ValueError:
        return {'error': f'Track with id={track_id} not found!'}, 400
    except Exception:
        return {'error': f'Failed to retrieve track with id={track_id}, internal error!'}, 500
    return TrackInfoResponse(track_id=track_id, track=track)
