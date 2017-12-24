
from api.main import welcome


# lambda function handler
def handler(event, context):
    ret_obj = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    body = welcome()
    ret_obj['body'] = body
    return ret_obj