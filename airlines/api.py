from ninja import Router

from airlines.schemas import AirplaneIn, ApiResponseInfo

router = Router()


@router.post('/airplane', tags=['v1'],
             response=ApiResponseInfo)
def post_aircraft(request, payload: AirplaneIn):
    """
    Adds one aircraft to the aircraft fleet.
    The aircraft ID must be from 1 to 10.
    """
    return ApiResponseInfo(code=200)


@router.get('/airplane/{identifier}',
            tags=['v1'],
            response=ApiResponseInfo)
def get_aircraft(request, identifier: int):
    """
    Generates Aircraft Specification.
    - fuel consumption per minute
    - maximum minutes able to fly
    """
    return ApiResponseInfo(code=200)
