import ConfigParser
import logging

import time

import boto3
from bottle import get, run

logging.basicConfig()
__logger = logging.getLogger(__name__)

@get('/healthcheck')
def healthcheck():
    return "Hello World!"

@get('/sleep/<secs>')
def sleep(secs):
    time.sleep(float(secs))
    return 'sleep for {} secs'.format(secs)

@get('/secret')
def get_secret():
    import os
    parser = ConfigParser.RawConfigParser()
    p = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'secret.ini')
    parser.read(p)
    region = parser.get('aws', 'region')
    var_name = parser.get('secret', 'var_name')
    client = boto3.client('ssm', region_name=region)
    secret = client.get_parameter(Name=var_name, WithDecryption=True)
    return secret


@get('/')
def welcome():
    return 'Welcome to my home'

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=False)