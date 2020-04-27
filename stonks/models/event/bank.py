from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from .base import Event
from stonks.enums import EventTypeEnum

class BankTransaction(Event):
    class Meta(Event.Meta):
        pass

    value = NumberAttribute()
    eventType = NumberAttribute(default=EventTypeEnum.BANK)
    

    