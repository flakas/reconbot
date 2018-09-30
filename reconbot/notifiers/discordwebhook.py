import json
import requests

class DiscordWebhookNotifier:
    def __init__(self, url):
        self.url = url

    def notify(self, text, options={}):
        return self._send_message(text)

    def _send_message(self, message):
        payload = {
            'content': message
        }
        return requests.post(self.url, json=payload)
