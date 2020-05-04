import ulid
import os
from .base import Consumer
from stonks.enums import EventTypeEnum, ActionEnum
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute


class SymbolIndex(GlobalSecondaryIndex):
    class Meta:
        projection = AllProjection()
    
    symbol = UnicodeAttribute(hash_key=True)

class Holding(Consumer):
    class Meta(Consumer.Meta):
        table_name = os.environ['STAGE'] + '-stonks-holding'
    
    holdingId = UnicodeAttribute(hash_key=True, default_for_new=str(ulid.new()))
    symbol = UnicodeAttribute(default="fresh")
    symbolIndex = SymbolIndex()
    units = NumberAttribute(default=0)
    averagePrice = NumberAttribute(default=0)
    latestTradePrice = NumberAttribute(default=0)
    bookCost = NumberAttribute(default=0)

    # Consumes the event
    @classmethod
    def consume(cls, event, consumer=None):
        if(consumer == None):
            symbol = event['symbol']
            results = cls.symbolIndex.query(symbol)
            results = [result for result in results]
            if(len(results) == 0):
                consumer = cls(symbol=symbol, holdingId=str(ulid.new()))
                consumer.save()
            else:
                consumer = results[0]

        consumer.refresh(consistent_read=True)
        
        # Bit of business logic
        action = event['action']
        units = int(event['units'])
        tradePrice = int(event['tradePrice'])
        holdingBookCost = int(consumer.averagePrice) * int(consumer.units)
        eventAveragePrice = int(event['averagePrice'])
        eventTotalCost = eventAveragePrice * units

        if(action == ActionEnum.BUY):
            units += int(consumer.units)             
            holdingBookCost +=  eventTotalCost
        elif(action == ActionEnum.SELL):
            units = int(consumer.units) - units
            holdingBookCost -= eventTotalCost
        
        try:
            averagePrice = int(holdingBookCost / units)
        except ZeroDivisionError:
            averagePrice = 0
        # Update fields
        consumer.update(
            actions=[
                cls.units.set(units),
                cls.averagePrice.set(averagePrice),
                cls.bookCost.set(holdingBookCost),
                cls.latestTradePrice.set(tradePrice),
                cls.version.set(event['eventId'])
            ]
        )


class Stock(Holding):
    class Meta(Holding.Meta):
        pass


class MutualFund(Holding):
    class Meta(Holding.Meta):
        pass

