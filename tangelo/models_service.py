#!/usr/bin/env python

#-----------------------------------------------------------------------
# models_service.py
#-----------------------------------------------------------------------

from sqlalchemy.types import TypeDecorator, Text
from sqlalchemy.ext import mutable
import json

#-----------------------------------------------------------------------

class JSONEncodedDict(TypeDecorator):
    """
    JSON encode dictionaries when added to a table. Decode on field access.

    Used for maintaining `grid_location` field in Subscription table.
    """
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

#-----------------------------------------------------------------------
