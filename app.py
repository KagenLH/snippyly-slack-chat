import os

from flask import Flask, request, current_app
from flask_sock import Sock
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
PORT = os.environ.get("PORT", 3000)

# Maintain the list of active connected clients so that we can send replies back to them outside the context of the socket listener
active_clients = set()
# Maintain a list of timestamps for messages that the bot has sent, that way we only send back replies to the bot's own messages.
message_timestamps = set()


app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

flask_app = Flask(__name__, static_url_path="")
sock = Sock(flask_app)
handler = SlackRequestHandler(app)


@app.event("message")
def respond_to_message(client, event, logger):
    message_text = event.get("text")
    thread_ts = event.get("thread_ts", None)
    if thread_ts is not None and thread_ts in message_timestamps:
        for client in active_clients:
            if client.connected:
                client.send(message_text)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/", methods=["GET"])
def serve_page():
    return current_app.send_static_file('index.html')


@sock.route('/websocket')
def listen_on_websocket(ws):
    active_clients.add(ws)
    while True:
        message = ws.receive()
        res = app.client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=message)
        message_timestamps.add(res.get("ts"))


if __name__ == "__main__":
    flask_app.run(port=PORT)
