from typing import Optional, cast

from airlines.v1.entities import AircraftSpecification
from airlines.v1.response_wrapper import server_response

from airlines.logreport import LogReport
from airlines.models import Airplane
from airlines.schemas import ApiResponseInfo
from django.shortcuts import get_object_or_404
from django.http.response import Http404


class GetAircraftUseCase:

    @server_response
    def __call__(self, identifier: int) -> ApiResponseInfo:
        with LogReport(name=self.__class__.__name__):
            if not (aircraft := self._get_aircraft(identifier)):
                text = f'Airplane with identifier {identifier} was not found.'
                return ApiResponseInfo(code=404, text=text)
            aircraft_spec = AircraftSpecification(airplane_identifier=aircraft.airplane_identifier,
                                                  passenger_capacity=aircraft.passenger_capacity)
            aircraft_spec.calculate_real_tank_capacity()
            aircraft_spec.calculate_real_consumption()
            aircraft_spec.calculate_flight_minutes()
            result = aircraft_spec.dict(include={'fuel_consumption', 'flight_minutes'})
            return ApiResponseInfo(code=200, results=result)

    @staticmethod
    def _get_aircraft(identifier: int) -> Optional[Airplane]:
        try:
            return cast(Airplane, get_object_or_404(Airplane, airplane_identifier=identifier))
        except Http404:
            return None
