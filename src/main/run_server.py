from src.main.service.replay_buffer_service import ReplayBufferService


def app():
    replay_buffer_service = ReplayBufferService()
    return replay_buffer_service.app()
