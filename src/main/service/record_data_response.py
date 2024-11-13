from enum import Enum


class RecordDataResponse(Enum):
    """
    Enum modeling possible responses to record data requests
    """

    OK = "Data recorded successfully."
    INVALID_SCHEMA = "Wrong Json Schema."
    INTERNAL_ERROR = "Internal Error."
