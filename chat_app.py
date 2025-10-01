import streamlit as st
import openai
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# App config
st.set_page_config(page_title="ChatGPT with Sidebar", page_icon="💬", layout="wide")

# CSS Styling for Avatars & Dark Mode Support
st.markdown("""
    <style>
        .chat-message {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1rem;
            padding: 0.8rem;
            border-radius: 0.5rem;
        }
        .user-message {
            background-color: #DCF8C6;
        }
        .assistant-message {
            background-color: #F1F0F0;
        }
        [data-theme="dark"] .assistant-message {
            background-color: #2d2d2d;
        }
        [data-theme="dark"] .user-message {
            background-color: #003e1f;
        }
        .avatar {
            font-size: 1.8rem;
        }
        .message-text {
            font-size: 1.1rem;
            line-height: 1.4;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "chats" not in st.session_state:
    st.session_state.chats = {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# Sidebar: chat history + new chat
st.sidebar.title("🧠 Chat History")
chat_titles = list(st.session_state.chats.keys())

selected_chat = st.sidebar.radio("Select chat:", chat_titles, index=chat_titles.index(st.session_state.current_chat))
st.session_state.current_chat = selected_chat

if st.sidebar.button("➕ New Chat"):
    new_title = f"Chat {len(st.session_state.chats)}"
    st.session_state.chats[new_title] = []
    st.session_state.current_chat = new_title
    st.experimental_rerun()

# Get current conversation
messages = st.session_state.chats[st.session_state.current_chat]

# Show messages
st.title("💬 ChatGPT Interface")

for msg in messages:
    role = msg["role"]
    content = msg["content"]
    avatar = "🧑" if role == "user" else "🤖"
    css_class = "user-message" if role == "user" else "assistant-message"

    st.markdown(
        f"""
        <div class='chat-message {css_class}'>
            <div class='avatar'>{avatar}</div>
            <div class='message-text'>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Chat input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("You:", key="input", height=80, label_visibility="collapsed", placeholder="Type your message...")
    submitted = st.form_submit_button("Send")

# Send message
if submitted and user_input.strip():
    messages.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        assistant_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": assistant_reply})
        st.experimental_rerun()
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
