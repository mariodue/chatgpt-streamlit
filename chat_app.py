import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Minimal ChatGPT", page_icon="💬", layout="centered")

st.markdown("""
    <style>
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .user-message {
            background-color: #DCF8C6;
            text-align: right;
        }
        .assistant-message {
            background-color: #F1F0F0;
            text-align: left;
        }
        .message-text {
            font-size: 1.1rem;
            line-height: 1.5;
        }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 Minimal ChatGPT")

for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]

    with st.container():
        css_class = "user-message" if role == "user" else "assistant-message"
        st.markdown(
            f"<div class='chat-message {css_class}'><div class='message-text'>{content}</div></div>",
            unsafe_allow_html=True
        )

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("You:", key="input", height=100, label_visibility="collapsed", placeholder="Type your message...")
    submit = st.form_submit_button("Send")

if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )

        assistant_reply = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        st.experimental_rerun()
    except Exception as e:
        st.error(f"API error: {e}")
