import streamlit as st
import chatbot as chat_backend  # Importing the file above
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# **************************************** Page Config ******************************
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

# Custom CSS for a better look
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        text-align: left;
        border-radius: 5px;
    }
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# **************************************** Session Setup ******************************

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = str(uuid.uuid4())

# **************************************** Utility Functions *************************

def start_new_chat():
    st.session_state['thread_id'] = str(uuid.uuid4())
    st.session_state['messages'] = []

def get_messages_for_thread(thread_id):
    """Fetches message history from LangGraph state."""
    config = {'configurable': {'thread_id': thread_id}}
    state = chat_backend.chatbot.get_state(config)
    return state.values.get('messages', [])

# **************************************** Sidebar UI *********************************

with st.sidebar:
    st.title("💬 Threads")
    
    if st.button("➕ New Chat", type="primary"):
        start_new_chat()
    
    st.markdown("---")
    st.caption("Recent Conversations")

    # Get all threads existing in DB
    existing_threads = chat_backend.get_all_thread_ids()

    # Sort threads? (Ideally by date, but simpler here just by list order)
    for t_id in existing_threads:
        # Get the human-readable title from our separate table
        title = chat_backend.get_thread_title(t_id)
        
        # Highlight the current active thread
        if t_id == st.session_state['thread_id']:
            st.markdown(f"**🔹 {title}**")
        else:
            if st.button(title, key=t_id):
                st.session_state['thread_id'] = t_id
                st.rerun()

# **************************************** Main Chat UI ******************************

st.subheader("LangGraph Assistant")

# Load current thread messages
current_messages = get_messages_for_thread(st.session_state['thread_id'])

# Display History
for msg in current_messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# Chat Input
if user_input := st.chat_input("Type your message here..."):
    
    # 1. Display User Message Immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Check if this is the FIRST message in this thread
    # If currently empty, we should generate a title after response
    is_first_message = len(current_messages) == 0

    # 3. Stream Assistant Response
    with st.chat_message("assistant"):
        stream_container = st.empty()
        full_response = ""
        
        config = {'configurable': {'thread_id': st.session_state['thread_id']}}
        
        # Stream logic
        for chunk, _ in chat_backend.chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages"
        ):
            if isinstance(chunk, AIMessage) and chunk.content:
                full_response += chunk.content
                stream_container.markdown(full_response + "▌")
        
        stream_container.markdown(full_response)

    # 4. Generate Title (If this was the first message)
    if is_first_message:
        with st.spinner("Generating conversation title..."):
            new_title = chat_backend.generate_chat_name(user_input)
            chat_backend.save_thread_title(st.session_state['thread_id'], new_title)
            st.rerun() # Rerun to update the sidebar title immediately