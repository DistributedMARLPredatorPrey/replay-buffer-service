from flask import Flask

from src.main.service.replay_buffer_service import ReplayBufferService


def app() -> Flask:
    """
    Creates a Replay buffer service
    :return: Flask app of the Replay buffer service
    """
    replay_buffer_service: ReplayBufferService = ReplayBufferService()
    return replay_buffer_service.app()
