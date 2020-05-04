from dynamodb_json import json_util as json
from stonks.enums import EventTypeEnum
from stonks.models.consumer.account import Account
from stonks.models.consumer.holding import Holding

# Tells the consumer to update itself on dynamodb event stream
def handler(event, context):
     parsedEvent = json.loads(event)
     for record in parsedEvent['Records']:
        if(record['eventName'] != 'INSERT'):
            return
        consumableEvent = record['dynamodb'].get('NewImage')
        eventType = consumableEvent['eventType']
        if(eventType == EventTypeEnum.TRADE):
            Holding.consume(event=consumableEvent)
            Account.consume(event=consumableEvent)
        elif(eventType == EventTypeEnum.BANK):
            Account.consume(event=consumableEvent)
    

