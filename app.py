from flask import Flask, send_from_directory
import os


app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(
        os.path.dirname(__file__),
        "app_index.html"
    )


@app.route("/api/disposal_data")
def disposal_data():
    return send_from_directory(
        os.path.dirname(__file__),
        "disposal_data.csv"
    )


@app.route("/api/transfer_data")
def transfer_data():
    return send_from_directory(
        os.path.dirname(__file__),
        "transfer_data.csv"
    )


@app.route("/api/transaction_data")
def transaction_data():
    return send_from_directory(
        os.path.dirname(__file__),
        "transaction_data.csv"
    )


if __name__ == '__main__':
    app.run(debug=True)
