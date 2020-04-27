from .base import Consumer
from stonks.enums import EventTypeEnum, ActionEnum
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute

class Holding(Consumer):
    class Meta(Consumer.Meta):
        pass

    # Consumes the event
    @classmethod
    def consume(cls, event, consumer=None):
        if(consumer == None):
            symbol = event['symbol']
            results = cls.scan(cls.symbol==symbol)
            results = [result for result in results]
            if(len(results) == 0):
                consumer = cls(symbol=symbol)
            else:
                consumer = results[0]

        # Bit of business logic
        action = event['action']
        units = int(event['units'])
        tradePrice = int(event['tradePrice'])
        holdingBookCost = int(consumer.averagePrice) * int(consumer.units)
        eventAveragePrice = int(event['averagePrice'])
        eventTotalCost = eventAveragePrice * units

        if(action == ActionEnum.BUY):
            units = int(consumer.units) + units
            holdingBookCost = (holdingBookCost + eventTotalCost)
        elif(action == ActionEnum.SELL):
            units = int(consumer.units) - units
            holdingBookCost = (holdingBookCost - eventTotalCost) 
        
        averagePrice = holdingBookCost / units
        # Update fields
        consumer.symbol = symbol
        consumer.units = int(units)
        consumer.latestTradePrice = tradePrice
        consumer.averagePrice = int(averagePrice)
        consumer.bookCost = int(holdingBookCost)

        # Update version
        consumer.version = event['eventId']

        # This actually does a PutItem
        consumer.save()
    
    symbol = UnicodeAttribute(default="fresh")
    units = NumberAttribute(default=0)
    averagePrice = NumberAttribute(default=0)
    latestTradePrice = NumberAttribute(default=0)
    bookCost = NumberAttribute()


class Stock(Holding):
    class Meta(Holding.Meta):
        pass


class MutualFund(Holding):
    class Meta(Holding.Meta):
        pass