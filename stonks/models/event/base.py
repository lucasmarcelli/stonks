import os
import ulid
from datetime import datetime
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

# The base event model.
class Event(Model):
    class Meta:
        table_name = os.environ['STAGE'] + '-stonks-event'
        region = 'ca-central-1'
        host = 'https://dynamodb.ca-central-1.amazonaws.com'
    
    eventId = UnicodeAttribute(hash_key=True, default_for_new=str(ulid.new()))
    # User defined datetime
    eventDateTime = UnicodeAttribute(range_key=True)
    eventType = NumberAttribute()
    createdAt = UTCDateTimeAttribute(default_for_new=datetime.now())

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))

    def save(self, conditional_operator=None, **expected_values):
        self.eventId = str(ulid.new())
        super(Event, self).save()

