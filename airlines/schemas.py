from typing import Any

from django.contrib.auth.models import User
from ninja import ModelSchema, Schema
from time import time as now_time


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username']


# ApiRequests
class AirplaneIn(Schema):
    airplane_identifier: int
    passenger_capacity: int


# ApiResponses

class ApiResponseInfo(Schema):
    created_at: int = now_time()
    results: Any = None
    text: str = ''
    code: int
