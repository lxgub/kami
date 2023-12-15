from functools import wraps

from airlines.logreport import get_logger
from airlines.schemas import ApiResponseInfo
from traceback import format_exc


def server_response(func):   # type: ignore
    @wraps(func)
    def wrapper(*args, **kwargs) -> tuple[int, ApiResponseInfo]:   # type: ignore
        try:
            r = func(*args, **kwargs)
            return r.code, r
        except Exception as ex:
            stacktrace = format_exc()
            text = f"{type(ex).__name__}: {str(ex)}"
            status = 500
            tb = dict(message=text, STACKTRACE=stacktrace)
            get_logger().error(f"{tb}")
        return 500, ApiResponseInfo(code=status, text=text)

    return wrapper
