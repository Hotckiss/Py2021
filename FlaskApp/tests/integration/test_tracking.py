import unittest

from lib.api import register, info
from lib.models import Track


class TestTracking(unittest.TestCase):
    def test_register_invalid_1(self):
        request = Track(
            name="name",
            project_id="project_id",
            max_parallel_pools=3,
            min_pool_acceptance_rate=-0.5,
            max_hourly_appeals=10,
            check_interval_minutes=5,
            soft_alert_multiplier=1.0
        )

        response = register(request)

        self.assertEqual(2, len(response))
        self.assertEqual(400, response[1])

    def test_register_invalid_2(self):
        request = Track(
            name="name",
            project_id="project_id",
            max_parallel_pools=-3,
            min_pool_acceptance_rate=0.5,
            max_hourly_appeals=10,
            check_interval_minutes=5,
            soft_alert_multiplier=1.0
        )

        response = register(request)

        self.assertEqual(2, len(response))
        self.assertEqual(400, response[1])

    def test_register_ok(self):
        request = Track(
            name="name",
            project_id="project_id",
            max_parallel_pools=3,
            min_pool_acceptance_rate=0.5,
            max_hourly_appeals=10,
            check_interval_minutes=5,
            soft_alert_multiplier=1.0
        )

        response = register(request)
        import re
        uuid4hex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)

        self.assertTrue(uuid4hex.search(response.id))

    def test_register_ok_info(self):
        request = Track(
            name="name",
            project_id="project_id",
            max_parallel_pools=3,
            min_pool_acceptance_rate=0.5,
            max_hourly_appeals=10,
            check_interval_minutes=5,
            soft_alert_multiplier=1.0
        )

        response = register(request)
        import re
        uuid4hex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)

        self.assertTrue(uuid4hex.search(response.id))

        resp_info = info(response.id)

        self.assertEqual(request.name, resp_info.track.name)

