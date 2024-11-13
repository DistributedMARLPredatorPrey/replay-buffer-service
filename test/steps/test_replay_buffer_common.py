from behave import *

from src.main.parser.config import ReplayBufferConfig
from src.main.service.replay_buffer_service import ReplayBufferService

use_step_matcher("re")


@given("The Replay Buffer is up and running")
def step_impl(context):
    config: ReplayBufferConfig = ReplayBufferConfig(
        num_predators=1,
        num_preys=1,
        num_states=2,
        num_actions=2,
        dataset_path="dataset.csv",
    )
    replay_buffer: ReplayBufferService = ReplayBufferService(config)
    context.conf = config
    context.client = replay_buffer.test_client()


@then("I should receive a 200 as response status")
def step_impl(context):
    assert context.response.status_code == 200
