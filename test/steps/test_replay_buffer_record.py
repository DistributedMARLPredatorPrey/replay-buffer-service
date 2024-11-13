import json
from typing import Dict, List

from behave import *
from werkzeug.test import TestResponse

from src.main.service.post_response import PostResponseStatus

use_step_matcher("re")


@step("I prepare an valid data record")
def prepare_valid_data_records(context):
    """
    Prepares a valid data record
    :type context: behave.runner.Context
    """
    valid_data_records: Dict[str, List[List[float]]] = {
        "State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Reward": [[1, 2], [1, 2]],
        "Action": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Next State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
    }
    context.data_record = valid_data_records


@step("I prepare an invalid data record")
def prepare_invalid_data_records(context):
    """
    Prepares an invalid data record
    :type context: behave.runner.Context
    """
    invalid_data_records: Dict[str, List[List[float]]] = {
        "State": [[1.0, 1.0], [1.1, 1.1, 2.1, 2.1]],
        "Reward": [[1, 2], [1, 2]],
        "Action": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Next State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
    }
    context.data_record = invalid_data_records


@when("I request this data to be recorded")
def record_data(context):
    """
    Records data inside the Replay Buffer
    :type context: behave.runner.Context
    """
    response: TestResponse = context.client.post(
        "record_data/", json=context.data_record
    )
    context.response = response


@then("the message should indicate successful operation")
def test_success_response(context):
    """
    Tests the previously made request is successful
    :type context: behave.runner.Context
    """
    assert context.response.text == json.dumps({"status": PostResponseStatus.OK.value})


@step("the message should indicate unsuccessful operation")
def test_invalid_schema_response(context):
    """
    Tests the previously made request to respond invalid schema
    :type context: behave.runner.Context
    """
    assert context.response.text == json.dumps(
        {"status": PostResponseStatus.INVALID_SCHEMA.value}
    )
