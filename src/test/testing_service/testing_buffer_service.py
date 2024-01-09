from src.main.service.buffer_service import BufferService


class TestingBufferService(BufferService):

    def test_client(self):
        self._app.config["TESTING"] = True
        self._app.test_client()