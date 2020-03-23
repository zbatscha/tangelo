from sqlalchemy.types import TypeDecorator, Text
from sqlalchemy.ext import mutable
import json
"""
Handling JSON columns. May be of use as we differentiate widgets.
"""
class JSONEncodedDict(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

mutable.MutableDict.associate_with(JSONEncodedDict)
