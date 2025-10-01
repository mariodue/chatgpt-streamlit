import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="ChatGPT Bootstrap", page_icon="💬", layout="wide")

# Inject Bootstrap CSS and custom styles
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
        /* Center the input form */
        .input-container {
            max-width: 600px;
            margin: 1rem auto 2rem;
        }
        /* Rounded textarea without square edges */
        textarea.form-control {
            border-radius: 20px !important;
            resize: none;
        }

        /* Sidebar button styling for equal width and no lines */
        .sidebar-btn {
            display: block !important;
            width: 100% !important;
            padding: 0.5rem 0 !important;
            margin-bottom: 0.5rem !important;
            border-radius: 0.375rem !important;
            border: none !important;
            box-shadow: none !important;
            background-color: #0d6efd !important;
            color: white !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            text-align: center !important;
            cursor: pointer !important;
            transition: background-color 0.15s ease-in-out !important;
        }
        .sidebar-btn:hover {
            background-color: #0b5ed7 !important;
            color: white !important;
        }
        .sidebar-btn:focus {
            outline: none !important;
            box-shadow: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "chats" not in st.session_state:
    st.session_state.chats = {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"
if "search_term" not in st.session_state:
    st.session_state.search_term = ""
if "show_search" not in st.session_state:
    st.session_state.show_search = False

# --- Sidebar Navigation ---
st.sidebar.markdown('<h4 class="mt-4">🧠 Navigation</h4>', unsafe_allow_html=True)

# Wrap buttons in a full-width container div
st.sidebar.markdown('<div style="width: 100%;">', unsafe_allow_html=True)

# New Chat button
if st.sidebar.button("➕ New Chat", key="new_chat", help="Start a new chat"):
    new_title = f"Chat {len(st.session_state.chats)}"
    st.session_state.chats[new_title] = []
    st.session_state.current_chat = new_title
    st.session_state.search_term = ""
    st.experimental_rerun()

# Search Chats toggle button
if st.sidebar.button("🔍 Search Chats", key="search_chat", help="Search your chats"):
    st.session_state.show_search = not st.session_state.show_search

# Close the container div
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Search expander popup
if st.session_state.show_search:
    with st.sidebar.expander("Search Chats", expanded=True):
        search_input = st.text_input("Type to search chats", value=st.session_state.search_term)
        st.session_state.search_term = search_input.strip().lower()

# JS to add sidebar-btn class to all buttons inside sidebar for uniform styling
st.sidebar.markdown("""
<script>
const buttons = window.parent.document.querySelectorAll('section[data-testid="stSidebar"] button');
buttons.forEach(btn => btn.classList.add('sidebar-btn'));
</script>
""", unsafe_allow_html=True)

# Filter chat titles based on search term
chat_titles = list(st.session_state.chats.keys())
if st.session_state.search_term:
    filtered_titles = [title for title in chat_titles if st.session_state.search_term in title.lower()]
else:
    filtered_titles = chat_titles

if not filtered_titles:
    st.sidebar.info("No chats found.")
    selected_chat = None
else:
    if st.session_state.current_chat in filtered_titles:
        default_index = filtered_titles.index(st.session_state.current_chat)
    else:
        default_index = 0
        st.session_state.current_chat = filtered_titles[0]
    selected_chat = st.sidebar.radio("Select chat:", filtered_titles, index=default_index)

st.session_state.current_chat = selected_chat

if selected_chat is None:
    st.write("Please create or select a chat.")
    st.stop()

messages = st.session_state.chats[selected_chat]

# Main title
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
