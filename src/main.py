from dotenv import load_dotenv

from config import GigachatConfig
from services.render.chat_render import ChatRenderService
from services.chatbot.gigachat import Gigachat


def main():
    load_dotenv(".env")
    config = GigachatConfig()
    chatbot = Gigachat(config)
    chat = ChatRenderService(chatbot)
    chat.render()


if __name__ == '__main__':
    main()
