from src.main.service.buffer_service import BufferService


def run_server():
    buffer_service = BufferService()
    return buffer_service.app()
