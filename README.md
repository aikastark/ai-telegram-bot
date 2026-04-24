# 🤖 AI Telegram Bot with RAG

A Telegram bot powered by OpenAI that can answer user questions using Retrieval-Augmented Generation (RAG) and maintain conversation memory.

## 🚀 Features

- Chat with AI directly in Telegram
- Uses OpenAI for natural language responses
- Retrieval-Augmented Generation (RAG) with FAISS
- Answers based on custom data (`data.txt`)
- Prevents hallucinations (answers only from context)
- Conversation memory per user

## 🛠 Tech Stack

- Python
- python-telegram-bot
- OpenAI API
- FAISS (vector search)
- NumPy

## 🧠 How it works

1. Loads text data from `data.txt`
2. Converts text into embeddings
3. Stores embeddings in FAISS vector database
4. On user message:
   - finds relevant chunks
   - sends context + question to OpenAI
5. AI generates answer based on context

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone <your-repo-link>
cd ai-telegram-bot
2. Create virtual environment
python -m venv venv
3. Install dependencies
venv\Scripts\python -m pip install -r requirements.txt
4. Create .env
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
▶️ Run
venv\Scripts\python bot.py
💬 Example questions
What is gingivitis?
What are flu symptoms?
What is cancer? (should return "I don't know")
⚠️ Note

This is a demo project and not intended for real medical use.