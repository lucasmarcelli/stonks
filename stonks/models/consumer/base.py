import os
import ulid
from datetime import datetime
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

# Consumers are only ever modified by events, queries only read them.
class Consumer(Model):
    class Meta:
        region = 'ca-central-1'
        host = 'https://dynamodb.ca-central-1.amazonaws.com'
    
    # A range key for sorting all consumers
    updatedAt = UTCDateTimeAttribute(range_key=True)
    createdAt = UTCDateTimeAttribute(default_for_new=datetime.now())

    # ULID of the last event that modified the consumer from the stream or a soft reconcile
    version = UnicodeAttribute(default_for_new="fresh")
    # ULID of the last event that the consumer hard reconciled to
    reconciledTo = UnicodeAttribute(default_for_new="fresh")

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(Consumer, self).save()