import os
import json

import requests
from slack_bolt import App

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

messages = []

@app.event("message")
def respond_to_message(client, event, logger):
    message_text = event.get("text")
    data=json.dumps({"msg": message_text})
    requests.post("http://localhost:8000/send-message", data=data, headers={"Content-Type": "application/json"})

if __name__ == "__main__":
    app.start(port=3000)