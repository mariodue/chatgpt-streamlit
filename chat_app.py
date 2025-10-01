import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="ChatGPT Bootstrap", page_icon="💬", layout="wide")

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* Chat styling */
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
        .input-container {
            max-width: 600px;
            margin: 1rem auto 2rem;
        }
        textarea.form-control {
            border-radius: 20px !important;
            resize: none;
        }

        /* Minimalistic sidebar buttons */
        .custom-sidebar-btn {
            width: 100%;
            margin-bottom: 0.5rem;
            border-radius: 0.375rem;
            padding: 0.5rem 0;
            font-size: 1rem;
            font-weight: 500;
            background-color: transparent !important;
            color: inherit !important;
            border: none !important;
            cursor: pointer;
            text-align: center;
            transition: background-color 0.15s ease-in-out;
            display: block;
        }
        .custom-sidebar-btn:hover {
            background-color: #e0e0e0 !important;
            color: inherit !important;
        }
        .custom-sidebar-btn:focus {
            outline: none !important;
            box-shadow: none !important;
        }
    </style>
""", unsafe_allow_html=True)

if "chats" not in st.session_state:
    st.session_state.chats = {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"
if "search_term" not in st.session_state:
    st.session_state.search_term = ""
if "show_search" not in st.session_state:
    st.session_state.show_search = False

st.sidebar.markdown('<h4 class="mt-4">🧠 Navigation</h4>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="width: 100%;">', unsafe_allow_html=True)

if st.sidebar.button("➕ New Chat", key="new_chat"):
    new_title = f"Chat {len(st.session_state.chats)}"
    st.session_state.chats[new_title] = []
    st.session_state.current_chat = new_title
    st.session_state.search_term = ""
    st.experimental_rerun()

if st.sidebar.button("🔍 Search Chats", key="search_chat"):
    st.session_state.show_search = not st.session_state.show_search

st.sidebar.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_search:
    with st.sidebar.expander("Search Chats", expanded=True):
        search_input = st.text_input("Type to search chats", value=st.session_state.search_term)
        st.session_state.search_term = search_input.strip().lower()

st.sidebar.markdown("""
<script>
const buttons = window.parent.document.querySelectorAll('section[data-testid="stSidebar"] button');
buttons.forEach(btn => {
    btn.classList.add('custom-sidebar-btn');
});
</script>
""", unsafe_allow_html=True)

chat_titles = list(st.session_state.chats.keys())
if st.session_state.search_term:
    filtered_titles = [t for t in chat_titles if st.session_state.search_term in t.lower()]
else:
    filtered_titles = chat_titles

if not filtered_titles:
    st.sidebar.info("No chats found.")
    selected_chat = None
else:
    if st.session_state.current_chat in filtered_titles:
        default_idx = filtered_titles.index(st.session_state.current_chat)
    else:
        default_idx = 0
        st.session_state.current_chat = filtered_titles[0]
    selected_chat = st.sidebar.radio("Select chat:", filtered_titles, index=default_idx)

st.session_state.current_chat = selected_chat

if selected_chat is None:
    st.write("Please create or select a chat.")
    st.stop()

messages = st.session_state.chats[selected_chat]

st.markdown("<h2 class='mt-3 text-center'>💬 ChatGPT Bootstrap Interface</h2>", unsafe_allow_html=True)

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
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    user_input = st.text_area("You:", key="input", height=80, label_visibility="collapsed", placeholder="Type your message...")
    st.markdown('</div>', unsafe_allow_html=True)
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    messages.append({"role": "user", "content": user_input})

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})
        st.experimental_rerun()
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
