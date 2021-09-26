import unittest

import numpy as np
from collections import defaultdict

from lib.models import TolokaPool
from lib.validation import check_project, check_pool


class TestValidation(unittest.TestCase):
    def test_check_pool_empty_1(self):
        self.assertTrue(check_pool(0, 0, 1))

    def test_check_pool_2(self):
        self.assertTrue(check_pool(1, 2, 0.3))

    def test_check_pool_3(self):
        self.assertTrue(check_pool(5, 1, 0.75))

    def test_check_project_one_pool(self):
        pools = [
            TolokaPool("id", "pid", "OPEN")
        ]

        self.assertTrue(check_project(pools, 1))

    def test_check_project_two_pools(self):
        pools = [
            TolokaPool("id", "pid", "OPEN"),
            TolokaPool("id2", "pid", "OPEN")
        ]

        self.assertFalse(check_project(pools, 1))
