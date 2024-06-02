from dotenv import load_dotenv
import streamlit as st
from config import GigachatConfig
from services.render.chat_render import ChatRenderService
from services.chatbot.gigachat import Gigachat


def main():
    load_dotenv(".env")
    st.set_page_config(
        page_title="SoftBananas GPT",
    )
    config = GigachatConfig()
    chatbot = Gigachat(config)
    chat = ChatRenderService(chatbot)
    chat.render()


if __name__ == '__main__':
    main()
