import json
from pynamodb.exceptions import DoesNotExist
from stonks.models.consumer.base import Consumer


def get(event, context):
    try:
        consumer = Consumer.get(hash_key=event['path']['consumerId'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'not found'})}
    except:
        return {'statusCode': 500,
                'body': json.dumps(event)}

    return {'event': dict(consumer)}