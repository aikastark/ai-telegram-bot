import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI
import faiss
import numpy as np

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TOKEN = os.getenv("TELEGRAM_TOKEN")

# ===== RAG =====
with open("data.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = [c.strip() for c in text.split("\n") if c.strip()]

embeddings = []
for chunk in chunks:
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    embeddings.append(emb.data[0].embedding)

dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


# ===== memory =====
user_memory = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    # --- search (RAG) ---
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=user_message
    ).data[0].embedding

    D, I = index.search(np.array([q_emb]), k=2)
    context_text = "\n".join([chunks[i] for i in I[0]])

    # --- память ---
    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({"role": "user", "content": user_message})

    messages = [
        {"role": "system", "content":
        """You are a medical assistant.
        Answer ONLY using the provided context.
        If the answer is not in the context, say: I don't know."""}
    ] + user_memory[user_id][-5:]

    messages.append({
        "role": "user",
        "content": f"Context:\n{context_text}\n\nQuestion: {user_message}"
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

    user_memory[user_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()