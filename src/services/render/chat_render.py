import streamlit as st

from services.chatbot.abstract import AbstractChatbot


class ChatRenderService:
    def __init__(self, bot: AbstractChatbot):
        self.bot = bot
        self.messages = [
            {
                "role": "ai",
                "content": {
                    "text": "Привет! Я специальный чат-бот "
                            "для компании SoftBananas inc. "
                            "на базе GigaChat.\nЖду вашего промптика :3",
                    "image": None
                }
            }
        ]
        if "messages" not in st.session_state:
            st.session_state.messages = self.messages
        if "access_token" not in st.session_state:
            try:
                st.session_state.access_token = self.bot.get_access_token()
                st.toast("Получен токен доступа к GigaChat API")
            except Exception as e:
                st.toast(f"Ошибка получения токена доступа к GigaChat API! {e}")

    def render(self):
        st.title("SoftBananas GPT")
        st.logo("static/images/logo.jpg")

        for message in st.session_state.messages:
            if message["content"]["image"]:
                st.chat_message("ai").image(message["content"]["image"])
            else:
                st.chat_message("ai").write(message["content"]["text"])

        if prompt := st.chat_input():
            st.chat_message("user").write(prompt)
            st.session_state.messages.append({"role": "user", "content": {"text": prompt, "image": None}})

            with st.spinner("Ща подумаю, сек..."):
                answer, image = self.bot.send_prompt(prompt)
            if image:
                st.chat_message("ai").image(image)
            else:
                st.chat_message("ai").write(answer)
            st.session_state.messages.append({"role": "ai", "content": {"text": answer, "image": image}})
