import time
from threading import Thread

from lib.models import TolokaProject
from lib.storage import storage
from lib.validation import track_project


def __monitor_iteration():
    tracks = storage.get_all_tracks()

    for track in tracks:
        if track_project(TolokaProject(track.project_id, "name"), track.max_parallel_pools):
            print("Alert! Too many running pools")


def __monitor():
    retries = 0
    while True:
        try:
            time.sleep(60)
            __monitor_iteration()
            retries = 0
        except Exception as e:
            retries += 1
            if retries == 3:
                retries = 0
                time.sleep(3600)


def start_tracking():
    subthread = Thread(name="tracker", target=__monitor)
    subthread.start()