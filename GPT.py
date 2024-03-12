import sys
import os
import json
import requests
import time

class TextProcessor:
    def __init__(self, api_key: str):
        """
        Ініціалізує об'єкт класу TextProcessor.

        Параметри:
            - api_key (str): Ключ API для OpenAI.
        """
        self.api_key = api_key

    def ask_question(self, question):
        headers = {"Authorization": f"Bearer {self.api_key}"}

        url = "https://api.edenai.run/v2/text/chat"
        payload = {
            "providers": "openai",
            "openai": "gpt-4",
            "text": question,
            "chatbot_global_action": "Act as an assistant",
            "previous_history": [],
            "temperature": 0.0,
            "max_tokens": 2500,
            "fallback_providers": ""
        }

        response = requests.post(url, json=payload, headers=headers)
        result = json.loads(response.text)
        time.sleep(0.5)


        result = json.loads(response.text)
        return result['openai']['generated_text']