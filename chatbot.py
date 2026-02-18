from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

# Shared LLM instance
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

# --- Graph Definition (Same as your original) ---
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Database Setup
DB_PATH = 'chatbot.db'
conn = sqlite3.connect(database=DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# --- Helper Functions for Titles & Storage ---

def init_title_db():
    """Creates a simple table to store thread names."""
    with sqlite3.connect(DB_PATH, check_same_thread=False) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS thread_titles (
                thread_id TEXT PRIMARY KEY,
                title TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.commit()

def save_thread_title(thread_id, title):
    with sqlite3.connect(DB_PATH, check_same_thread=False) as c:
        c.execute("""
            INSERT OR REPLACE INTO thread_titles (thread_id, title, updated_at) 
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (str(thread_id), title))
        c.commit()

def update_thread_timestamp(thread_id):
    """Updates the timestamp for a thread to mark it as recently active."""
    with sqlite3.connect(DB_PATH, check_same_thread=False) as c:
        c.execute("""
            UPDATE thread_titles 
            SET updated_at = CURRENT_TIMESTAMP 
            WHERE thread_id = ?
        """, (str(thread_id),))
        c.commit()

def get_thread_title(thread_id):
    with sqlite3.connect(DB_PATH, check_same_thread=False) as c:
        cursor = c.execute("SELECT title FROM thread_titles WHERE thread_id = ?", (str(thread_id),))
        result = cursor.fetchone()
        return result[0] if result else "New Chat"

def get_all_thread_ids():
    """Retrieves all thread IDs known to the checkpointer, sorted by most recent first."""
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    
    # Sort by timestamp from our titles table (most recent first)
    with sqlite3.connect(DB_PATH, check_same_thread=False) as c:
        cursor = c.execute("""
            SELECT thread_id FROM thread_titles 
            ORDER BY updated_at DESC
        """)
        sorted_threads = [row[0] for row in cursor.fetchall()]
    
    # Add any threads that exist in checkpoint but not in titles table
    for thread_id in all_threads:
        if thread_id not in sorted_threads:
            sorted_threads.append(thread_id)
    
    return sorted_threads

def generate_chat_name(user_message_content):
    """Uses LLM to generate a short title based on the first message."""
    system_prompt = "You are a helpful assistant. Summarize the following user message into a short, 4-5 word phrase to be used as a chat title. Do not use quotes."
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message_content)
    ]
    response = llm.invoke(messages)
    return response.content.strip()

# Initialize the title table on import
init_title_db()