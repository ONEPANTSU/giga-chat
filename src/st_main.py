"""
File to deploy via Streamlit
"""

import streamlit as st
from config import GigachatConfig
from services.render.chat_render import ChatRenderService
from services.chatbot.gigachat import Gigachat


def main():
    st.set_page_config(
        page_title="SoftBananas GPT",
    )
    config = GigachatConfig(
        client_id=st.secrets["GIGACHAT_CLIENT_ID"],
        client_secret=st.secrets["GIGACHAT_CLIENT_SECRET"],
    )
    chatbot = Gigachat(config)
    chat = ChatRenderService(chatbot)
    chat.render()


if __name__ == '__main__':
    main()
