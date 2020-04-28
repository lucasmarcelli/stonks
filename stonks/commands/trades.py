import json
import os
import time
import sys
import boto3

from stonks.enums import ActionEnum
from stonks.models.event.trade import Trade
from stonks.models.consumer.holding import Holding

def create(event, context):
    data = json.loads(event['body'])  
    units = int(data['units'])  
    commission = int(data['commission']) if 'commission' in data else 99900
    action = data['action']
    averagePrice = units * int(data['tradePrice'])
    if(action == ActionEnum.BUY):
        averagePrice += commission
    else:
        averagePrice -= commission
    averagePrice = int(averagePrice / units)
    trade = Trade(
        commission=commission, 
        units=data['units'], 
        action=action,
        holdingType=data['holdingType'],
        symbol=data['symbol'],
        tradePrice=data['tradePrice'],
        averagePrice=averagePrice
    )
    trade.save()
    return {
        'statusCode': 200,
        'body': json.dumps(dict(trade))
    }


