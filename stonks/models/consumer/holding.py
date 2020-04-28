import ulid
from .base import Consumer
from stonks.enums import EventTypeEnum, ActionEnum
from pynamodb.indexes import LocalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute

class HoldingIndex(LocalSecondaryIndex):
    class Meta:
        projection = AllProjection()
    consumerId = UnicodeAttribute(hash_key=True)
    symbol = UnicodeAttribute(range_key=True)

class Holding(Consumer):
    class Meta(Consumer.Meta):
        pass

    # Consumes the event
    @classmethod
    def consume(cls, event, consumer=None):
        if(consumer == None):
            symbol = event['symbol']
            results = cls.scan(cls.symbol==symbol, consistent_read=True)
            results = [result for result in results]
            if(len(results) == 0):
                consumer = cls(symbol=symbol, consumerId=str(ulid.new()))
                consumer.save()
            else:
                consumer = results[0]

        consumer.refresh()
        
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
                cls.latestTradePrice.set(tradePrice)
            ]
        )

        super(Holding, cls).consume(event=event, consumer=consumer)
    
    symbol = UnicodeAttribute(default="fresh")
    units = NumberAttribute(default=0)
    averagePrice = NumberAttribute(default=0)
    latestTradePrice = NumberAttribute(default=0)
    bookCost = NumberAttribute(default=0)


class Stock(Holding):
    class Meta(Holding.Meta):
        pass


class MutualFund(Holding):
    class Meta(Holding.Meta):
        pass