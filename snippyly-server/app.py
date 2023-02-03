import os
import json

import requests
from flask import Flask, request
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

messages = []
clients = []

SLACK_API_URL = os.environ.get("SLACK_API_URL")

@sock.route('/websocket')
def echo_socket(ws):
    clients.append(ws)
    while True:
        message = ws.receive()
        data = json.dumps({"text": message})
        requests.post(SLACK_API_URL, data=data, headers={"Content-Type": "application/json"})


@app.route('/send-message', methods=['POST'])
def hello():
    try:
        message = request.json['msg']
        for client in clients:
            client.send(message)
    except Exception as e:
        print("Something went wrong... ", e)
    return "OK"


if __name__ == "__main__":
    app.run(port=8000)
