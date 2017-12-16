import logging

import time
from bottle import get, run

logging.basicConfig()
__logger = logging.getLogger(__name__)

@get('/healthcheck')
def healthcheck():
    return "Hello World!"

@get('/sleep/<secs>')
def sleep(secs=20):
    time.sleep(secs)
    return 'sleep for {} secs'.format(secs)

@get('/secret')
def get_secret():
    import os
    p = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'secret.txt')
    secret = None
    with open(p, 'rb') as f:
        secret = f.read()
    return secret


@get('/')
def welcome():
    return 'Welcome to my home'

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=False)