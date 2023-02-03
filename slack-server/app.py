import asyncio
import os

from slack_bolt import App
from snippyly_adapter import SnippylyAdapter

# app = App(
#     token=os.environ.get("SLACK_BOT_TOKEN"),
#     signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
# )

# @app.event("message.channels")
# def respond_to_message(client, event, logger):
#     message = {
#         "messageText": event.text
#     }
#     SnippylyAdapter.send_message(message)


if __name__ == "__main__":
    # app.start(port=int(os.environ.get("PORT", 3000)))
    asyncio.run(SnippylyAdapter.start_server())
    