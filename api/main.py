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

_SECRET_NAME = 'SECRET_NAME'
_REGION = 'REGION'

@get('/secret')
def get_secret():
    region = None
    secret = None
    import os
    # get parms from env vars first
    if _SECRET_NAME in os.environ:
        secret = os.environ[_SECRET_NAME]
        region = os.environ[_REGION]
    else:
        # otherwise, get from secret.ini
        parser = ConfigParser.RawConfigParser()
        p = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'secret.ini')
        parser.read(p)
        region = parser.get('aws', 'region')
        secret = parser.get('secret', 'var_name')

    return _get_secret(secret, region)

def _get_secret(secret_name, region_name):
    client = boto3.client('ssm', region_name=region_name)
    response = client.get_parameter(Name=secret_name, WithDecryption=False)
    secret = response['Parameter']['Value']
    # decrypt data here
    from base64 import b64decode
    secret = boto3.client('kms', region_name=region_name).decrypt(CiphertextBlob=b64decode(secret))['Plaintext']
    return {'Name': secret_name, 'Value': secret}


@get('/')
def welcome():
    return 'Welcome to my home'

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=False)