from typing import Optional

from pydantic import BaseModel, validator
from decimal import Decimal


class AircraftSpecification(BaseModel):
    airplane_identifier: int
    passenger_capacity: int

    base_tank_capacity: int = 200
    base_fuel_factor: Decimal = Decimal("0.8")
    passenger_fuel_factor: Decimal = Decimal("0.002")

    real_tank_capacity: Optional[int] = None
    fuel_consumption: Optional[Decimal] = None
    flight_minutes: Optional[Decimal] = None

    @validator('airplane_identifier')
    def airplane_identifier_validation(cls, value: int) -> int:
        """
        Validates the airplane_identifier value.
        """
        if 1 <= value <= 10:
            return value
        raise ValueError('The "plain_identifier" value must be between 1 and 10.')

    @validator('passenger_capacity')
    def passenger_capacity_validation(cls, value: int) -> int:
        """
        Validates the passenger_capacity value.
        """
        if value >= 1:
            return value
        raise ValueError('The "passenger_capacity" cannot be less than 1. '
                         'Our airplane is a passenger aircraft.')
