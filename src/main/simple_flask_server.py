from flask import Flask, request, jsonify
from markupsafe import escape

app = Flask(__name__)


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route('/record_data', methods=['POST'])
def record_data():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify({'message': 'JSON received successfully'})


if __name__ == '__main__':
    app.run()
