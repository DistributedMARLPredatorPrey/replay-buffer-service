from enum import Enum


class PostResponseStatus(Enum):
    OK = "Data recorded successfully."
    INVALID_SCHEMA = "Wrong Json Schema."
    INTERNAL_ERROR = "Internal Error."
