import os.path

from behave import *
from flask import Flask

from src.main.parser.config import ReplayBufferConfig
from src.main.service.replay_buffer_service import ReplayBufferService

use_step_matcher("re")


@given("The Replay Buffer is up and running")
def setup_replay_buffer(context):
    """
    Configures and starts the Replay Buffer service.
    :type context: behave.runner.Context
    """
    config: ReplayBufferConfig = ReplayBufferConfig(
        num_predators=1,
        num_preys=1,
        num_states=2,
        dataset_path=os.path.join("test", "resources", "dataset.csv"),
    )
    replay_buffer: ReplayBufferService = ReplayBufferService(config)
    app: Flask = replay_buffer.app
    app.config["TESTING"] = True
    # Set context variables
    context.conf = config
    context.client = app.test_client()


@then("I should receive a 200 as response status")
def test_response_ok(context):
    """
    Tests if the response status of the previous request is OK: 200.
    :type context: behave.runner.Context
    """
    assert context.response.status_code == 200
