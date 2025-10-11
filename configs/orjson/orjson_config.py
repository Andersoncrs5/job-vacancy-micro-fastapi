import orjson
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date, datetime
import json


def orjson_default(obj):
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, (date, datetime)):
        return str(obj)
    return json.JSONEncoder().default(obj)


def orjson_dumps(v, *, default=orjson_default):
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def model_dump_json(self, **kwargs):
        return orjson_dumps(self.model_dump(**kwargs))
