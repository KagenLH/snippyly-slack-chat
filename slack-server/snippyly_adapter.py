import asyncio
import os

import websockets


class SnippylyAdapter:
    @staticmethod
    async def send_message(websocket):
        async for message in websocket:
            print(message)
            await websocket.send("Replying to your message...")
    
    @staticmethod
    async def start_server():
        async with websockets.serve(SnippylyAdapter.send_message, "localhost", os.environ.get("PORT", 3000)):
            await asyncio.Future()
