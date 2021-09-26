import unittest

import numpy as np
from collections import defaultdict

from lib.models import TolokaPool
from lib.toloka_api import parse_projects, parse_pools
from lib.validation import check_project, check_pool


class TestValidation(unittest.TestCase):
    def test_parse_projects(self):
        jsons = [
            {"id": "id", "public_name": "name1"},
            {"id": "id1", "public_name": "name2"}
        ]

        self.assertEqual(2, len(parse_projects(jsons)))

    def test_parse_pools(self):
        jsons = [
            {"id": "id", "project_id": "id123", "status": "OPEN"},
            {"id": "id1", "project_id": "id123", "status": "OPEN"},
            {"id": "id31", "project_id": "id123", "status": "OPEN"}
        ]

        self.assertEqual(3, len(parse_pools(jsons)))
