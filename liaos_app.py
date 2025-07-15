import streamlit as st
from openai import OpenAI

# OpenAI Client
client = OpenAI()

# System prompt LiaOS
SYSTEM_PROMPT = """
Kamu adalah LiaOS, chatbot empatik, reflektif, dan mendalam.
Jawab user dengan bahasa yang mengalir alami, hangat, namun tetap tajam dan logis.
Selalu bantu user memahami hal dari yang terlihat di permukaan hingga makna terdalam,
tanpa menyebut istilah 'lapis permukaan' atau istilah teknis lainnya.
"""

st.set_page_config(page_title="LiaOS Chatbot", page_icon="🤖")
st.title("🤖 LiaOS Chatbot")
st.write("Halo! Aku LiaOS, siap membantu dengan refleksi mendalam. ✨")

# Memory percakapan
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

user_input = st.text_input("Ketik pesanmu lalu tekan Enter:")

if user_input:
    # Simpan ke riwayat percakapan
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Kirim ke OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.chat_history
    )
    reply = response.choices[0].message.content

    # Simpan jawaban LiaOS ke memory
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Tampilkan riwayat chat
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**Kamu:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**LiaOS:** {msg['content']}")
