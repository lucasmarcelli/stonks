from .base import Consumer
from stonks.enums import EventTypeEnum
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute

# 10000 = $1
# 1000 = 10 cents
# 100 = 1 cent
# 10 = 0.1 cent
class Cash(Consumer):
    class Meta(Consumer.Meta):
        pass

    current_value = NumberAttribute(default=0)





