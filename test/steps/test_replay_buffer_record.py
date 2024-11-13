import json
from typing import Dict, List

from behave import *
from werkzeug.test import TestResponse

from src.main.parser.config import ReplayBufferConfig
from src.main.service.post_response import PostResponseStatus
from src.main.service.replay_buffer_service import ReplayBufferService

use_step_matcher("re")


@step("I prepare an valid data record")
def step_impl(context):
    valid_data_record: Dict[str, List[List[float]]] = {
        "State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Reward": [[1, 2], [1, 2]],
        "Action": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Next State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
    }
    context.data_record = valid_data_record


@step("I prepare an invalid data record")
def step_impl(context):
    invalid_data_record: Dict[str, List[List[float]]] = {
        "State": [[1.0, 1.0], [1.1, 1.1, 2.1, 2.1]],
        "Reward": [[1, 2], [1, 2]],
        "Action": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Next State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
    }
    context.data_record = invalid_data_record


@when("I request this data to be recorded")
def step_impl(context):
    response: TestResponse = context.client.post(
        "record_data/", json=context.data_record
    )
    context.response = response


@then("the message should indicate successful operation")
def step_impl(context):
    assert context.response.text == json.dumps({"status": PostResponseStatus.OK.value})


@step("the message should indicate unsuccessful operation")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.response.text == json.dumps(
        {"status": PostResponseStatus.INVALID_SCHEMA.value}
    )
