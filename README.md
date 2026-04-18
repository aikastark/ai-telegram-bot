# AI Telegram Bot

Simple Telegram bot that sends user messages to OpenAI and replies with the model output.

## Requirements

- Python 3.12
- Telegram bot token
- OpenAI API key

## Setup

Install dependencies:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create a `.env` file with:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

## Run

```powershell
.\venv\Scripts\python.exe .\bot.py
```
