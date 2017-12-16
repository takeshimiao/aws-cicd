import os
import unittest

import datetime

from api.main import healthcheck, welcome, sleep, get_secret


class MainTest(unittest.TestCase):

    def test_healthcheck(self):
        self.assertEqual('Hello World!', healthcheck())

    def test_welcome(self):
        self.assertEqual('Welcome to my home', welcome())

    def test_sleep(self):
        secs = 5
        st = datetime.datetime.utcnow()
        msg = sleep(secs)
        et = datetime.datetime.utcnow()
        tdiff = et - st
        self.assertTrue(tdiff.seconds >= 5)
        self.assertEqual('sleep for {} secs'.format(secs), msg)

    def test_get_secret(self):
        secret = get_secret()
        p = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../api/conf', 'secret.txt')
        with open(p, 'rb') as f:
            expected = f.read()
        self.assertEqual(expected, secret)

