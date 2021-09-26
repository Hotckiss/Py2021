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
        return TolokaProject(json_dict['id'], json_dict['public_name'])


class TolokaPool:
    id: str
    project_id: str
    status: str

    def __init__(self, id, project_id, status):
        self.id = id
        self.project_id = project_id
        self.status = status

    @staticmethod
    def from_json(json_dict):
        return TolokaPool(json_dict['id'], json_dict['project_id'], PoolStatus[json_dict['status']])


class PoolStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    LOCKED = "LOCKED"
    ARCHIVED = "ARCHIVED"
