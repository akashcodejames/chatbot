# 🤖 AI Chatbot with LangGraph & Streamlit

A powerful conversational AI chatbot built with LangGraph, OpenAI's GPT-4, and Streamlit. Features persistent conversation threads with SQLite storage and automatic chat title generation.

## ✨ Features

- 💬 **Interactive Chat Interface** - Clean, modern Streamlit UI
- 🧵 **Thread Management** - Create and switch between multiple conversation threads
- 💾 **Persistent Storage** - SQLite-based conversation history
- 🎯 **Smart Titles** - Automatic AI-generated conversation titles
- ⚡ **Streaming Responses** - Real-time AI response streaming
- 🔄 **State Management** - LangGraph checkpoint system for conversation state

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Framework**: LangGraph + LangChain
- **LLM**: OpenAI GPT-4o-mini
- **Database**: SQLite with SqliteSaver checkpointer
- **Environment**: Python 3.9+

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/akashcodejames/chatbot.git
   cd chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🎮 Usage

1. **Activate the virtual environment**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the application**
   ```bash
   streamlit run frontend.py
   ```

3. **Access the application**
   
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
chatbot_OPENAi/
├── frontend.py              # Streamlit UI application
├── chatbot.py              # LangGraph chatbot logic & database
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not in git)
├── chatbot.db            # SQLite database (created on first run)
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)

### Model Configuration

By default, the chatbot uses `gpt-4o-mini`. To change the model, edit `chatbot.py`:

```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
```

## 📝 Features in Detail

### Thread Management
- Create new conversation threads with the "New Chat" button
- Switch between existing threads from the sidebar
- Each thread maintains its own conversation history

### Automatic Titles
- First message in each thread generates a descriptive title
- Titles are AI-generated based on conversation context
- Easy identification of conversations in the sidebar

### Persistent Storage
- All conversations stored in SQLite database
- Resume conversations anytime
- Thread state managed by LangGraph checkpointer

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Akash Yadav**
- GitHub: [@akashcodejames](https://github.com/akashcodejames)

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [OpenAI](https://openai.com/)
- UI with [Streamlit](https://streamlit.io/)

---

⭐ If you find this project useful, please consider giving it a star!
