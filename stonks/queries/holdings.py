import json
from pynamodb.exceptions import DoesNotExist
from stonks.models.consumer.holding import Holding

def list(event, context):
    try:
        results = Holding.scan(consistent_read=True)
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'not found'})}
                
    return {'holdings': [dict(result) for result in results]}
    

def get(event, context):
    try:
        holding = Holding.get(hash_key=event['path']['consumerId'], consistent_read=True)
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'not found'})}

    return {'holding': dict(holding)}


def getBySymbol(event, context):
    holdings = Holding.scan(symbol=event['querystring']['symbol'], consistent_read=True)
    holding = [dict(result) for result in holdings][0]
    return {'holding': dict(holding)}