import math

from dcd.entities.property_type import PropertyType
from datetime import datetime

class Property:
    """"A DCD 'Property' represents a numerical property of a Thing."""

    def __init__(self,
                 property_id=None,
                 name=None,
                 description=None,
                 property_type=None,
                 dimensions=(),
                 json_property=None,
                 values=(),
                 entity=None):

        self.subscribers = []

        if json_property is not None:
            self.property_id = json_property['id']
            self.name = json_property['name']
            self.description = json_property['description']
            self.property_type = PropertyType[json_property['type']]
            self.dimensions = json_property['dimensions']
            self.values = json_property['values']
        else:
            self.property_id = property_id
            self.name = name
            self.description = description
            self.property_type = property_type
            self.dimensions = dimensions
            self.values = values

    def to_json(self):
        p = {}
        if self.property_id is not None:
            p["id"] = self.property_id
        if self.name is not None:
            p["name"] = self.name
        if self.description is not None:
            p["description"] = self.description
        if self.property_type is not None:
            p["type"] = self.property_type.name
        if self.dimensions is not None and len(self.dimensions) > 0:
            p["dimensions"] = self.dimensions
        if self.values is not None and len(self.values) > 0:
            p["values"] = self.values
        return p

    def value_to_json(self):
        p = {}
        if self.property_id is not None:
            p["id"] = self.property_id
        if self.values is not None and len(self.values) > 0:
            p["values"] = self.values
        return p

    def belongs_to(self, entity):
        self.entity = entity

    def update_values(self, values, time_ms=None):
        ts = time_ms
        if ts is None:
            dt = datetime.utcnow()
            ts = unix_time_millis(dt)

        values_with_ts = [ts]
        values_with_ts.extend(values)

        # TODO: Remove the following line to accumulate local history
        # (it requires more advanced sync management)
        self.values = []
        self.values.append(values_with_ts)
        self.entity.update_property(self)

    def read(self, from_ts=None, to_ts=None):
        self.entity.read_property(self.property_id, from_ts, to_ts)

    def subscribe(self, uri):
        self.subscribers.append(uri)

def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return math.floor((dt - epoch).total_seconds() * 1000.0)
