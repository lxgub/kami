from ninja import Router

from airlines.schemas import AirplaneIn, ApiResponseInfo
from airlines.v1.get_aircraft import GetAircraftUseCase
from airlines.v1.post_aircraft import PostAircraftUseCase

router = Router()


@router.post('/aircraft', tags=['v1'],
             response={200: ApiResponseInfo,
                       404: ApiResponseInfo,
                       500: ApiResponseInfo})
def post_aircraft(request, payload: AirplaneIn):  # type: ignore
    """
    Adds one aircraft to the aircraft fleet.
    - We have only 10 types of aircraft [2,3,4,5,6,7,8,9,10,11]
    - The "airplane_identifier" must be from 2 to 11
    """
    return PostAircraftUseCase()(payload)


@router.get('/aircraft/{identifier}',
            tags=['v1'],
            response={200: ApiResponseInfo,
                      404: ApiResponseInfo,
                      500: ApiResponseInfo})
def get_aircraft(request, identifier: int):   # type: ignore
    """
    Generates Aircraft Specification.
    - fuel consumption per minute
    - maximum minutes able to fly
    """
    return GetAircraftUseCase()(identifier=identifier)
