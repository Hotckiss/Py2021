import typing
import uuid

from lib.models import Track


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

    def get_all_tracks(self) -> typing.List[Track]:
        return list(self.mem.values())


storage = InMemTrackStorage()
