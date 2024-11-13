from typing import Dict, List

import pandas as pd
import json
from behave import *
from werkzeug.test import TestResponse

use_step_matcher("re")


@when("I record a data batch of N rows")
def record_data_batch(context):
    """
    Record 10 data rows inside the Replay Buffer
    :type context: behave.runner.Context
    """
    data: Dict[str, List[List[float]]] = {
        "State": [[1.0, 1.0, 2.0, 2.0]],
        "Reward": [[1, 2]],
        "Action": [[1.0, 1.0, 2.0, 2.0]],
        "Next State": [[1.0, 1.0, 2.0, 2.0]],
    }
    context.record_size = 10
    for _ in range(context.record_size):
        context.client.post("record_data/", json=data)


@step("I request to receive a data data batch of M rows, where M>N")
def get_data_batch_empty(context):
    """
    Get a data batch from the Replay Buffer.
    The requested size (number of rows) is greater than the current dataset's
    :type context: behave.runner.Context
    """
    context.batch_size = 50
    assert context.record_size < context.batch_size
    response: TestResponse = context.client.get(f"batch_data/{context.batch_size}")
    context.response = response


@step("the received data batch should be empty")
def test_empty_data_batch(context):
    """
    Tests if the previously received data is empty
    :type context: behave.runner.Context
    """
    assert pd.DataFrame(json.loads(context.response.text)).shape[0] == 0


@step("I request to receive a data data batch of M rows, where M<=N")
def get_data_batch_nonempty(context):
    """
    Get a data batch from the Replay Buffer.
    The requested size (number of rows) is less than the current dataset's
    :type context: behave.runner.Context
    """
    context.batch_size = 5
    assert context.record_size >= context.batch_size
    response: TestResponse = context.client.get(f"batch_data/{context.batch_size}")
    context.response = response


@step("the received data batch should be nonempty")
def test_nonempty_data_batch(context):
    """
    Tests if the previously received data is nonempty
    :type context: behave.runner.Context
    """
    assert pd.DataFrame(json.loads(context.response.text)).shape[0] > 0


@step("the received data batch should have M rows")
def test_data_batch_size(context):
    """
    Tests if the previously received data has the requested size
    :type context: behave.runner.Context
    """
    assert (
        pd.DataFrame(json.loads(context.response.text)).shape[0] == context.batch_size
    )
