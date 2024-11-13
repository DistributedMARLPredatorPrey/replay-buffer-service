from typing import Dict, List

import pandas as pd
import json
from behave import *
from werkzeug.test import TestResponse

use_step_matcher("re")


@when("I record a data batch of N rows")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    data: Dict[str, List[List[float]]] = {
        "State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Reward": [[1, 2], [1, 2]],
        "Action": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
        "Next State": [[1.0, 1.0, 2.0, 2.0], [1.1, 1.1, 2.1, 2.1]],
    }
    context.record_size = 10
    for _ in range(context.record_size):
        context.client.post("record_data/", json=data)


@step("I request to receive a data data batch of M rows, where M>N")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.batch_size = 50
    assert context.record_size < context.batch_size
    response: TestResponse = context.client.get(f"batch_data/{context.batch_size}")
    context.response = response


@step("the received data batch should be empty")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert pd.DataFrame(json.loads(context.response.text)).shape[0] == 0


@step("I request to receive a data data batch of M rows, where M<=N")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.batch_size = 5
    assert context.record_size >= context.batch_size
    response: TestResponse =  context.client.get(f"batch_data/{context.batch_size}")
    context.response = response

@step("the received data batch should be nonempty")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert pd.DataFrame(json.loads(context.response.text)).shape[0] > 0


@step("the received data batch should have M rows")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert pd.DataFrame(json.loads(context.response.text)).shape[0] == context.batch_size
