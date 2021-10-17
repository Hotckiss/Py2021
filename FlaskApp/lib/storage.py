import typing
import uuid
import sqlite3
from lib.models import Track


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def get_db(path):
    conn = create_connection(path)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS tracks (
    	id text PRIMARY KEY,
    	name text NOT NULL,
        project_id text NOT NULL,
        max_parallel_pools INTEGER NOT NULL,
        min_pool_acceptance_rate NUMBER NOT NULL,
        max_hourly_appeals INTEGER NOT NULL,
        check_interval_minutes INTEGER NOT NULL,
        soft_alert_multiplier NUMBER NOT NULL
    )""")

    return conn


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


class SQLiteTrackStorage:
    @staticmethod
    def from_path(path):
        return SQLiteTrackStorage(get_db(path))

    def __init__(self, conn):
        self.conn = conn
        self.db: sqlite3.Cursor = conn.cursor()

    def insert_with_id(self, tid: str, track: Track) -> str:
        self.db.execute("INSERT INTO tracks (id, name, project_id, max_parallel_pools, min_pool_acceptance_rate, \
        max_hourly_appeals, check_interval_minutes, soft_alert_multiplier) \
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)", \
                        (tid, track.name, track.project_id, track.max_parallel_pools, \
                         track.min_pool_acceptance_rate, track.max_hourly_appeals, track.check_interval_minutes,
                         track.soft_alert_multiplier))

        self.conn.commit()
        return tid

    def insert(self, track: Track) -> str:
        return self.insert_with_id(str(uuid.uuid4()), track)

    def get(self, tid: str) -> Track:
        self.db.execute("SELECT * FROM tracks WHERE id=?", (tid,))

        rows = self.db.fetchall()

        if len(rows) == 0:
            raise ValueError("Requested track not found!")

        row = rows[0]
        result = Track(
            name=row[1],
            project_id=row[2],
            max_parallel_pools=row[3],
            min_pool_acceptance_rate=row[4],
            max_hourly_appeals=row[5],
            check_interval_minutes=row[6],
            soft_alert_multiplier=row[7]
        )

        return result

    def get_all_tracks(self) -> typing.List[Track]:
        self.db.execute("SELECT * FROM tracks")

        rows = self.db.fetchall()

        result = []
        for row in rows:
            result.append(Track(
                name=row[1],
                project_id=row[2],
                max_parallel_pools=row[3],
                min_pool_acceptance_rate=row[4],
                max_hourly_appeals=row[5],
                check_interval_minutes=row[6],
                soft_alert_multiplier=row[7]
            ))

        return result

    def clear(self):
        self.db.execute("DELETE FROM tracks")
        self.conn.commit()


storage = InMemTrackStorage()
