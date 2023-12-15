from airlines.v1.entities import AircraftSpecification
from airlines.v1.response_wrapper import server_response

from airlines.logreport import LogReport
from airlines.models import Airplane
from airlines.schemas import ApiResponseInfo, AirplaneIn


class PostAircraftUseCase:

    @server_response
    def __call__(self, airplane_in: AirplaneIn) -> ApiResponseInfo:
        with LogReport(name=self.__class__.__name__):
            aircraft_spec = self._get_spec(airplane_in)
            self._post_aircraft(aircraft_spec)
            return ApiResponseInfo(code=200)

    @staticmethod
    def _get_spec(airplane_in: AirplaneIn) -> AircraftSpecification:
        return AircraftSpecification(**airplane_in.dict())

    @staticmethod
    def _post_aircraft(data: AircraftSpecification) -> None:
        Airplane.objects.update_or_create(airplane_identifier=data.airplane_identifier,
                                          defaults=data.dict(include={'airplane_identifier',
                                                                      'passenger_capacity'}))
