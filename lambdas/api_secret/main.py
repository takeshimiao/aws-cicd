import json
import os

from api.main import _get_secret


secret_name = os.environ['SECRET_NAME']
region_name = os.environ['REGION']


# lambda function handler
def handler(event, context):
    ret_obj = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    body = _get_secret(secret_name, region_name)
    ret_obj['body'] = json.dumps(body)
    return ret_obj