
from api.main import healthcheck

# lambda function handler
def handler(event, context):
    ret_obj = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    body = healthcheck()
    ret_obj['body'] = body
    return ret_obj