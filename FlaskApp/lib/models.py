from enum import Enum

from pydantic import BaseModel


class Track(BaseModel):
    name: str
    project_id: str
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


class TolokaProject:
    id: str
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def from_json(json_dict):
        TolokaProject(json_dict['id'], json_dict['public_name'])


class TolokaPool:
    id: str
    project_id: str
    status: str

    def __init__(self, json_dict):
        self.id = json_dict['id']
        self.project_id = json_dict['project_id']
        self.status = PoolStatus['status']


class PoolStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    LOCKED = "LOCKED"
    ARCHIVED = "ARCHIVED"
