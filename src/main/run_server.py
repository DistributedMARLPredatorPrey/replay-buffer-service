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
        predator_dataset_path=replay_buffer_config.predator_dataset_path,
        prey_dataset_path=replay_buffer_config.prey_dataset_path,
    )
    return replay_buffer_service.app()
