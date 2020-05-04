import os
import ulid
from .base import Consumer
from stonks.models.event.trade import Trade
from stonks.enums import EventTypeEnum, ActionEnum
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

class NameIndex(GlobalSecondaryIndex):
    class Meta:
        projection = AllProjection()
    
    accountName = UnicodeAttribute(hash_key=True)

# 10000 = $1
# 1000 = 10 cents
# 100 = 1 cent
# 10 = 0.1 cent
class Account(Consumer):
    class Meta(Consumer.Meta):
        table_name = os.environ['STAGE'] + '-stonks-accounts'

    @classmethod
    def consume(cls, event, consumer=None):
        print(event)
        accountName = event['accountName']
        if(consumer == None):
            results = cls.nameIndex.query(name)
            if(len(results) == 0):
                consumer = cls(accountName=accountName, accountId=str(ulid.new())
            else:
                consumer = results[0]
        consumer.refresh(consistent_read=True)
        eventType = event['eventType']
        if(eventType == EventTypeEnum.BANK):
            value = int(event['value'])
        elif(eventType == EventTypeEnum.TRADE):
            action = event['action']
            units = int(event['units'])
            averagePrice = int(event['averagePrice'])
            averagePrice *= units
            if(action == ActionEnum.BUY):
                averagePrice *= -1
            value = averagePrice

        consumer.update(
            actions=[
                cls.currentValue.set(consumer.currentValue + value),
                cls.version.set(event['eventId'])
            ]
        )
        

    accountId = UnicodeAttribute(hash_key=True, default_for_new=str(ulid.new()))
    accountName = UnicodeAttribute()
    nameIndex = NameIndex()
    currentValue = NumberAttribute(default=0)

