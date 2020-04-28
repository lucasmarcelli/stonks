import json
from pynamodb.exceptions import DoesNotExist
from stonks.models.event.base import Event


def get(event, context):
    try:
        returnEvent = Event.get(hash_key=event['path']['eventId'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'not found'})}
    except:
        return {'statusCode': 500,
                'body': json.dumps(event)}

    return {'event': dict(returnEvent)}