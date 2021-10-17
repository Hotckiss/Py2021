import unittest

from lib.models import Track
from lib.storage import SQLiteTrackStorage, get_db


class TestTracking(unittest.TestCase):
    def test_insert(self):
        request = Track(
            name="name",
            project_id="project_id",
            max_parallel_pools=3,
            min_pool_acceptance_rate=-0.5,
            max_hourly_appeals=10,
            check_interval_minutes=5,
            soft_alert_multiplier=1.0
        )

        db = get_db("test_db.sqlite3")
        storage = SQLiteTrackStorage(db)
        storage.clear()

        storage.insert_with_id("id1", request)

        self.assertEqual(request, storage.get("id1"))

    def test_insert_2(self):
        request = Track(
            name="name",
            project_id="project_id",
            max_parallel_pools=3,
            min_pool_acceptance_rate=-0.5,
            max_hourly_appeals=10,
            check_interval_minutes=5,
            soft_alert_multiplier=1.0
        )

        request1 = Track(
            name="name1",
            project_id="project_id",
            max_parallel_pools=3,
            min_pool_acceptance_rate=-0.5,
            max_hourly_appeals=10,
            check_interval_minutes=5,
            soft_alert_multiplier=1.0
        )

        db = get_db("test_db.sqlite3")
        storage = SQLiteTrackStorage(db)
        storage.clear()

        storage.insert_with_id("id1", request)
        storage.insert_with_id("id2", request1)

        self.assertEqual(request, storage.get("id1"))
        self.assertEqual(request1, storage.get("id2"))

    def test_get_all(self):
        request = Track(
            name="name",
            project_id="project_id",
            max_parallel_pools=3,
            min_pool_acceptance_rate=-0.5,
            max_hourly_appeals=10,
            check_interval_minutes=5,
            soft_alert_multiplier=1.0
        )

        request1 = Track(
            name="name1",
            project_id="project_id",
            max_parallel_pools=3,
            min_pool_acceptance_rate=-0.5,
            max_hourly_appeals=10,
            check_interval_minutes=5,
            soft_alert_multiplier=1.0
        )

        db = get_db("test_db.sqlite3")
        storage = SQLiteTrackStorage(db)
        storage.clear()

        storage.insert_with_id("id1", request)
        storage.insert_with_id("id2", request1)

        self.assertEqual(2, len(storage.get_all_tracks()))

