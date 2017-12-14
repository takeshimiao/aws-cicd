import unittest

from api.main import healthcheck, welcome


class MainTest(unittest.TestCase):

    def test_healthcheck(self):
        self.assertEqual('Hello World!', healthcheck())

    def test_welcome(self):
        self.assertEqual('Welcome to my home', welcome())
