from flask import Flask

from src.main.parser.yaml_config_parser import YamlConfigParser
from src.main.service.replay_buffer_service import ReplayBufferService
import logging

logging.getLogger().setLevel(logging.INFO)

# Create a Replay buffer service and get the Flask App
replay_buffer_config = YamlConfigParser().replay_buffer_configuration()
replay_buffer_service: ReplayBufferService = ReplayBufferService(
    config=replay_buffer_config
)
app: Flask = replay_buffer_service.app
