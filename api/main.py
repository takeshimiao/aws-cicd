import logging

from bottle import get, run

logging.basicConfig()
__logger = logging.getLogger(__name__)

@get('/healthcheck')
def healthcheck():
    return "Hello World!"

@get('/')
def welcome():
    return 'Welcome to my home'

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=False)