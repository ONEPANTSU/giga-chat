import json
import re
import uuid

import requests
from requests.auth import HTTPBasicAuth

from services.chatbot.abstract import AbstractChatbot
from config import GigachatConfig


class Gigachat(AbstractChatbot):

    def __init__(self, config: GigachatConfig):
        self.config = config

    def send_prompt(self, prompt: str) -> tuple[str, bytes | None]:
        access_token = self.get_access_token()
        answer = self.__get_answer_message(access_token, prompt)
        image = self.__get_image(access_token, answer)
        return answer, image

    def get_access_token(self) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
        }
        payload = {
            "scope": "GIGACHAT_API_PERS"
        }
        response = requests.post(
            url=url,
            headers=headers,
            auth=HTTPBasicAuth(self.config.client_id, self.config.client_secret),
            data=payload,
            verify=False
        )
        return response.json()["access_token"]

    def __get_image(self, access_token: str, text: str) -> bytes | None:
        image_uuid = self.__get_image_uuid(text)
        if image_uuid is None:
            return None
        url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{image_uuid}/content"
        headers = {
            'Accept': 'image/jpg',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url=url, headers=headers, verify=False)
        return response.content

    @staticmethod
    def __get_image_uuid(text: str) -> str | None:
        pattern = r'src="([^"]+)"'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None

    def __get_answer_message(self, access_token: str, prompt: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        payload = json.dumps({
            "model": "GigaChat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "function_call": "auto"
        })
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(url=url, headers=headers, data=payload, verify=False)
        return response.json()["choices"][0]["message"]["content"]
