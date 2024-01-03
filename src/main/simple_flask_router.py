from flask import request, jsonify, Flask
from markupsafe import escape


class SimpleFlaskRouter:

    def __init__(self, app: Flask):
        """
        Init a SimpleFlaskRouter
        """
        self.app = app

        @self.app.route("/batch_data/<size>")
        def batch_data():
            return f"Hello, {escape(self)}!"

        @self.app.route("/record_data", methods=["POST"])
        def record_data():
            if request.method == "POST":
                data = request.get_json()
                print(data)
                return jsonify({"message": "JSON received successfully"})
