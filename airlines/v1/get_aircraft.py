from typing import Optional, cast

from airlines.v1.calculations import BaseAircraftCalculator
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
            calculator = BaseAircraftCalculator(airplane_identifier=aircraft.airplane_identifier,
                                                passenger_capacity=aircraft.passenger_capacity)
            calculator.calculate()
            results = calculator.get_result()
            return ApiResponseInfo(code=200, results=results)

    @staticmethod
    def _get_aircraft(identifier: int) -> Optional[Airplane]:
        try:
            return cast(Airplane, get_object_or_404(Airplane, airplane_identifier=identifier))
        except Http404:
            return None
