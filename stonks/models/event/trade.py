from datetime import datetime
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from stonks.enums import EventTypeEnum
from .base import Event

class Trade(Event):
    class Meta(Event.Meta):
        pass
    
    units = NumberAttribute()
    action = NumberAttribute()
    holdingType = NumberAttribute()
    symbol = UnicodeAttribute()
    tradePrice = NumberAttribute()
    averagePrice = NumberAttribute()
    commission = NumberAttribute()
    eventType = NumberAttribute(default=EventTypeEnum.TRADE)