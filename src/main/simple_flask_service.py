from threading import Thread

from flask import Flask, request, jsonify
from markupsafe import escape


class SimpleFlaskService:
    def __init__(self):
        """
        Init a SimpleFlaskApp
        """
        self.app = Flask(__name__)

        @self.app.route("/batch_data/<size>")
        def batch_data():
            return f"Hello, {escape(self)}!"

        @self.app.route("/record_data", methods=["POST"])
        def record_data():
            if request.method == "POST":
                data = request.get_json()
                print(data)
                return jsonify({"message": "JSON received successfully"})

    def run(self, ip, port):
        Thread(target=self.app.run, args=(ip, port)).start()
