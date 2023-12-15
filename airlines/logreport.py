from __future__ import annotations

import json
import logging
from time import time as now_time
from typing import Any, Dict

global_logger = None


def get_logger(loglevel=logging.INFO) -> Any:   # type: ignore
    """
    Get a global logger instance with the specified log level.

    :param loglevel: Log level to set for the logger.
    :return: Logger instance.
    """
    global global_logger
    if not global_logger:
        logging.basicConfig(
            format=u"%(asctime)s  %(levelname)s: %(message)s",
            level=loglevel)
        global_logger = logging
    return global_logger


class LogReport:
    """
    Initialize a LogReport instance.

    :param name: Name of the API method.
    :param logger: Logger for reporting operation details.
    :param api_response: API response object, defaults to None.
    :param **kwparams: Additional parameters to include in the report.
    """

    def __init__(self,
                 name: str,
                 logger: Any = get_logger(),
                 api_response: Any = None,
                 **kwparams: Any):
        """Initialization.

        :param str name: Name of the API method.
        :param logger: Logger for reporting operation details.
        :param **kwparams: Parameters to include in the report.
        """
        self._start_time = now_time()
        self._name = name
        self._params = kwparams.copy()
        self._logger = logger
        self._api_response = api_response

    def append(self, **kwparams: Dict[str, Any]) -> None:
        """
        Append additional key-value pairs to the report parameters.

        :param **kwparams: Key-value pairs to append to the report.
        """
        self._params.update(kwparams)

    def rename_key(self, name_old: Any, name_new: Any) -> LogReport:
        """
        Rename a key in the report parameters.

        :param name_old: Old key name.
        :param name_new: New key name.
        :return: Updated LogReport instance.
        """
        if name_old in self._params:
            self._params[name_new] = self._params.pop(name_old)
        return self

    def log(self) -> None:
        """
        Log the report data using the configured logger.
        """
        result_params_str = json.dumps(self._log_data(), ensure_ascii=False)
        self._logger.info(f"KAMI-REPORT: {result_params_str}")

    def _log_data(self) -> Dict[str, Any]:
        """Prints a report to the log.

        :param **kwparams: Other parameters to include in the report.
        """
        log_dict: Dict[str, Any] = self._params.copy()
        log_dict.update({
            "name": self._name,
            "execution_time": (now_time() - self._start_time)
        })
        return log_dict

    def __enter__(self) -> LogReport:
        """
        Enter context manager.

        :return: LogReport instance.
        """
        return self

    def __exit__(self,
                 exception_type: Any,
                 exception_value: Any,
                 trace: Any) -> Any:
        """
        Exit the context manager.

        :param exception_type: Type of exception.
        :param exception_value: Value of exception.
        :param trace: Traceback information.
        """
        if self._api_response:
            self._params['status'] = self._api_response.status
            self._params['created_at'] = self._api_response.created_at
        self.log()
        return False
