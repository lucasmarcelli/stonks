import json
from pynamodb.exceptions import DoesNotExist
from stonks.models.consumer.account import Account

def getAll(event, context):
    try:
        accounts = Account.scan(consistent_read=True)
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'not found'})}
    except:
        return {'statusCode': 500,
                'body': json.dumps(accounts)}

    return {'accounts': [dict(result) for result in accounts]}