import json
import os
import time
import sys
import boto3

from stonks.models.event.bank import BankTransaction

def create(event, context):
    data = json.loads(event['body'])    
    if 'value' not in data:
        return {
            'statusCode': 400,
            'message': 'send value bruh'
        }
    transaction = BankTransaction(value=data['value'])
    transaction.save()
    return {
        'statusCode': 200,
        'body': json.dumps(dict(transaction))
    }

