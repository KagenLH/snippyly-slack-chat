import os

import requests

class SnippylyAdapter:
    SNIPPYLY_API_URL = os.environ.get("SNIPPYLY_API_URL")
    
    @staticmethod
    def send_message(self, message):
        try:
            requests.post(self.SNIPPYLY_API_URL, data=message)
        except requests.RequestException as e:
            print(f"Something went wrong with the request to the Snippyly API... exception message: {e}")
