from typing import Optional, Union

from pydantic import BaseModel, validator
import math
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

    # VALIDATION:
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

    # CALCULATION:
    def calculate_real_tank_capacity(self) -> None:
        """
        Calculates the real tank capacity based on the airplane_identifier.
        """
        self.real_tank_capacity = self.airplane_identifier * self.base_tank_capacity

    def calculate_real_consumption(self) -> None:
        """
        Calculates the fuel consumption in minutes.
        """
        base_consumption = self._get_base_consumption()
        additional_consumption = self._get_additional_consumption()
        self.fuel_consumption = base_consumption + additional_consumption

    def calculate_flight_minutes(self) -> None:
        """
        Calculates maximum flight duration in minutes based
        on real_tank_capacity and fuel_consumption.
        """
        if self.fuel_consumption and self.real_tank_capacity:
            self.flight_minutes = self.real_tank_capacity / self.fuel_consumption

    def _get_base_consumption(self) -> Decimal:
        """
        Calculates the base fuel consumption using
        the logarithm of the airplane_identifier.
        """
        logarithm = self._get_math_log(self.airplane_identifier)
        return logarithm * self.base_fuel_factor

    @staticmethod
    def _get_math_log(number: Union[int, float, Decimal]) -> Decimal:
        """
        Returns the logarithm of the given number.
        """
        return Decimal(math.log(number))

    def _get_additional_consumption(self) -> Decimal:
        """
        Calculates the additional fuel consumption
        based on passenger_capacity and passenger_fuel_factor.
        """
        return self.passenger_capacity * self.passenger_fuel_factor
