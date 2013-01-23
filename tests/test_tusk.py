# -*- coding: utf-8  -*-
import os

from unittest import TestCase

from tusk import Lock


class TuskTest(TestCase):
    def setUp(self):
        dsn = os.environ.get("DATABASE_URL")
        self.former = Lock(dsn or "postgres://localhost/tusk")
        self.latter = Lock(dsn or "postgres://localhost/tusk")

    def test_acquire_release(self):
        self.former.acquire("tusk_release")
        self.assertTrue(not self.latter.acquire("tusk_release", blocking=False))
        self.assertTrue(self.former.release("tusk_release"))
        self.assertTrue(self.latter.acquire("tusk_release", blocking=False))
