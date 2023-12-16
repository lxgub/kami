import math
from typing import Protocol, Dict, Union

from airlines.v1.entities import AircraftSpecification
from decimal import Decimal


class IAircraftCalculator(Protocol):

    def calculate(self) -> None:
        ...

    def get_result(self) -> Dict:
        ...


class BaseAircraftCalculator(IAircraftCalculator):

    def __init__(self,
                 airplane_identifier: int,
                 passenger_capacity: int) -> None:
        self._specification = AircraftSpecification(airplane_identifier=airplane_identifier,
                                                    passenger_capacity=passenger_capacity)

    def calculate(self) -> None:
        self._calculate_real_tank_capacity()
        self._calculate_real_consumption()

    def get_result(self) -> Dict:
        return self._specification.dict(include={'fuel_consumption', 'flight_minutes'})

    def _calculate_real_tank_capacity(self) -> None:
        """
        Calculates the real tank capacity based on the airplane_identifier.
        """
        self._specification.real_tank_capacity = \
            self._specification.airplane_identifier * self._specification.base_tank_capacity

    def _calculate_real_consumption(self) -> None:
        """
        Calculates the fuel consumption in minutes.
        """
        base_consumption = self._get_base_consumption()
        additional_consumption = self._get_additional_consumption()
        self.fuel_consumption = base_consumption + additional_consumption

    def _calculate_flight_minutes(self) -> None:
        """
        Calculates maximum flight duration in minutes based
        on real_tank_capacity and fuel_consumption.
        """
        if self._specification.fuel_consumption and self._specification.real_tank_capacity:
            self._specification.flight_minutes = \
                self._specification.real_tank_capacity / self._specification.fuel_consumption

    def _get_base_consumption(self) -> Decimal:
        """
        Calculates the base fuel consumption using
        the logarithm of the airplane_identifier.
        """
        logarithm = self._get_math_log(self._specification.airplane_identifier)
        return logarithm * self._specification.base_fuel_factor

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
        return self._specification.passenger_capacity * self._specification.passenger_fuel_factor
