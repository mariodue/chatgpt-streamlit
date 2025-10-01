import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="ChatGPT Bootstrap", page_icon="💬", layout="wide")

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .chat-container {
            padding: 20px;
        }
        .chat-card {
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            max-width: 80%;
        }
        .chat-avatar {
            font-size: 1.8rem;
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

if "chats" not in st.session_state:
    st.session_state.chats = {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

st.sidebar.markdown('<h4 class="mt-4">🧠 Chat History</h4>', unsafe_allow_html=True)

chat_titles = list(st.session_state.chats.keys())
selected_chat = st.sidebar.radio("Select chat:", chat_titles, index=chat_titles.index(st.session_state.current_chat))
st.session_state.current_chat = selected_chat

if st.sidebar.button("➕ New Chat"):
    new_title = f"Chat {len(st.session_state.chats)}"
    st.session_state.chats[new_title] = []
    st.session_state.current_chat = new_title
    st.experimental_rerun()

messages = st.session_state.chats[st.session_state.current_chat]

st.markdown("<h2 class='mt-3'>💬 ChatGPT Bootstrap Interface</h2>", unsafe_allow_html=True)

def render_message(role, content):
    is_user = role == "user"
    avatar = "🧑" if is_user else "🤖"
    align_class = "ms-auto text-end" if is_user else "me-auto text-start"
    bg_class = "bg-success-subtle" if is_user else "bg-light-subtle"
    text_color = "text-dark"

    st.markdown(f"""
        <div class="d-flex {align_class}">
            <div class="chat-card {bg_class} {text_color} shadow-sm d-flex">
                <div class="chat-avatar">{avatar}</div>
                <div>{content}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in messages:
        render_message(msg["role"], msg["content"])
    st.markdown("</div>", unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("You:", key="input", height=80, label_visibility="collapsed", placeholder="Type your message...")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    messages.append({"role": "user", "content": user_input})

    try:
        response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        )

        )
        assistant_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": assistant_reply})
        st.experimental_rerun()
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
