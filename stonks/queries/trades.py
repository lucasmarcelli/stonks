import json
from pynamodb.exceptions import DoesNotExist
from stonks.models.event.trade import Trade

def list(event, context):
    try:
        results = Trade.scan()
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'not found'})}
    except:
        return {'statusCode': 500,
                'body': json.dumps(event)}
                
    return {'trades': [dict(result) for result in results]}
    

def get(event, context):
    try:
        trade = Trade.get(hash_key=event['path']['eventId'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'not found'})}
    except:
        return {'statusCode': 500,
                'body': json.dumps(event)}

    return {'trade': dict(trade)}