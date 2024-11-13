import json
from enum import Enum


class RecordDataResponseStatus(Enum):
    """
    Enum modeling possible responses to record data requests
    """

    OK = "Data recorded successfully."
    INVALID_SCHEMA = "Wrong Json Schema."
    INTERNAL_ERROR = "Internal Error."


class RecordDataResponse:
    """
    Record Data Batch Response
    """

    def __init__(self, status: RecordDataResponseStatus):
        self.__status = status
        self.text: str = json.dumps({"status": status.value})
