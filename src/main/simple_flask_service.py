from multiprocessing import Process

from flask import Flask, request, jsonify
from markupsafe import escape


class SimpleFlaskService:

    def __init__(self, ip, port):

        app = Flask(__name__)

        @app.route("/batch_data/<size>")
        def batch_data(size):
            return f"Hello, {escape(size)}!"

        @app.route('/record_data', methods=['POST'])
        def record_data():
            if request.method == 'POST':
                data = request.get_json()
                print(data)
                return jsonify({'message': 'JSON received successfully'})

        self._server = Process(target=app.run, args=(ip, port))

    def run(self):
        self._server.start()

    def stop(self):
        self._server.terminate()
        self._server.join()
