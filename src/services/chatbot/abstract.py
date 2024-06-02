from abc import ABC, abstractmethod


class AbstractChatbot(ABC):
    @abstractmethod
    def send_prompt(self, prompt: str):
        raise NotImplementedError

    @abstractmethod
    def get_access_token(self) -> str:
        raise NotImplementedError
