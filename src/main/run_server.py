from flask import Flask

from src.main.parser.yaml_config_parser import YamlConfigParser
from src.main.service.replay_buffer_service import ReplayBufferService
import logging

logging.getLogger().setLevel(logging.INFO)


def app() -> Flask:
    """
    Creates a Replay buffer service
    :return: Flask app of the Replay buffer service
    """
    replay_buffer_config = YamlConfigParser().replay_buffer_configuration()
    replay_buffer_service: ReplayBufferService = ReplayBufferService(
        config=replay_buffer_config,
    )
    return replay_buffer_service.app()
