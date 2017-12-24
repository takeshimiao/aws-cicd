
from api.main import sleep


# lambda function handler
def handler(event, context):
    secs = event['pathParameters']['secs']
    body = sleep(secs)
    ret_obj = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    ret_obj['body'] = body
    return ret_obj