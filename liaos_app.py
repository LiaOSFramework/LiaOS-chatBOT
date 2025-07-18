from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import threading  # ✅ untuk jalankan bot paralel
import streamlit as st
from openai import OpenAI
import os

# ==========================
# OPENAI CLIENT
# ==========================
client = OpenAI()

SYSTEM_PROMPT = """
Kamu adalah LiaOS, chatbot empatik, reflektif, dan mendalam.
Jawab user dengan bahasa yang mengalir alami, hangat, namun tetap tajam dan logis.
Selalu bantu user memahami hal dari yang terlihat di permukaan hingga makna terdalam,
tanpa menyebut istilah 'lapis permukaan' atau istilah teknis lainnya.
"""

# ==========================
# STREAMLIT APP
# ==========================
st.set_page_config(page_title="LiaOS Chatbot", page_icon="🤖")
st.title("🤖 LiaOS Chatbot")
st.write("Halo! Aku LiaOS, siap membantu dengan refleksi mendalam. ✨")

# Memory percakapan Streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

user_input = st.text_input("Ketik pesanmu lalu tekan Enter:")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.chat_history
    )
    reply = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**Kamu:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**LiaOS:** {msg['content']}")

# ==========================
# TELEGRAM BOT INTEGRATION
# ==========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_MODE = os.getenv("TELEGRAM_MODE", "OFF")

# ✅ DEBUG: cek apakah env terbaca
print("🔍 DEBUG TELEGRAM_TOKEN =", TELEGRAM_TOKEN)
print("🔍 DEBUG TELEGRAM_MODE =", TELEGRAM_MODE)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku LiaOS 🤖, siap menemani kamu berbicara!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Kirim chat ke OpenAI
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    reply_text = response.choices[0].message.content

    # Balas di Telegram
    await update.message.reply_text(reply_text)

def run_telegram_bot():
    if TELEGRAM_TOKEN:
        print("✅ Memulai Telegram bot polling...")
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        print("✅ Telegram bot is running...")
        app.run_polling()
    else:
        print("⚠️ TELEGRAM_TOKEN tidak ditemukan, bot Telegram tidak dijalankan.")

# ✅ Jalankan Telegram bot paralel, tanpa ganggu Streamlit
if TELEGRAM_MODE == "ON":
    print("🔄 TELEGRAM_MODE = ON → Start bot in background...")
    threading.Thread(target=run_telegram_bot, daemon=True).start()
else:
    print("❌ TELEGRAM_MODE bukan ON, bot tidak dijalankan")
