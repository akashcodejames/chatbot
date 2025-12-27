# AI Chatbot

A conversational AI chatbot built with LangGraph, OpenAI's GPT-4, and Streamlit. Features persistent conversation threads with automatic title generation.

## Features

- 💬 Interactive chat interface with streaming responses
- 🧵 Multiple conversation threads with thread management
- 💾 Persistent SQLite-based conversation history
- 🎯 AI-generated conversation titles
- 🔄 Latest conversations appear first in sidebar
- ⚡ Real-time response streaming

## Tech Stack

- **Frontend**: Streamlit
- **AI Framework**: LangGraph + LangChain
- **LLM**: OpenAI GPT-4o-mini
- **Database**: SQLite with SqliteSaver checkpointer

## Installation

1. Clone the repository:
```bash
git clone https://github.com/akashcodejames/chatbot.git
cd chatbot
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

Run the application:
```bash
streamlit run frontend.py
```

Open your browser at `http://localhost:8501`

## Project Structure

```
chatbot/
├── frontend.py          # Streamlit UI
├── chatbot.py          # LangGraph logic & database
├── requirements.txt    # Dependencies
├── .env               # API key (create this)
└── chatbot.db        # SQLite database (auto-created)
```

## How It Works

- **New Chat**: Creates a new conversation thread
- **First Message**: Automatically generates a descriptive title
- **Thread Sorting**: Active threads appear at the top
- **Persistence**: All conversations saved and can be resumed anytime
