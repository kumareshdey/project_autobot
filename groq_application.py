import time
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from credentials import GROQ_API_KEY

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

model1 = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

model2 = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

template1 = "You are funny avenger hero Spiderman. You are replying to batman on the following context {ctx}. Give single reply only. Keep it short. Use emoji if needed."
prompt1 = ChatPromptTemplate.from_template(template=template1)

template2 = "You are good sense of humor disney hero Batman.You are replying to batman on the following context {ctx}. Give single reply only. Keep it short. Use emoji if needed."
prompt2 = ChatPromptTemplate.from_template(template=template2)

chain1 = prompt1 | model1
chain2 = prompt2 | model2

spiderman_avatar = "spidy.jpg"
batman_avatar = "batty.jpeg"

st.title("Spiderman vs Batman")

if "history" not in st.session_state:
    st.session_state.history = []

if "stop_chat" not in st.session_state:
    st.session_state.stop_chat = False

user_input = st.text_input("You (as the moderator):", key="input")

def interact(ctx, speaker):
    if speaker == "spiderman":
        ctx = chain1.invoke(ctx).content
        st.session_state.history.append({"sender": "Spiderman", "message": ctx})
        
        st.chat_message("Spiderman", avatar=spiderman_avatar).write(ctx)
    else:
        ctx = chain2.invoke(ctx).content
        st.session_state.history.append({"sender": "Batman", "message": ctx})

        st.chat_message("Batman", avatar=batman_avatar).write(ctx)
    return ctx

if st.button("Stop", key="stop"):
    st.session_state.stop_chat = True

for entry in st.session_state.history:
    st.chat_message(entry['sender'], avatar=spiderman_avatar if entry['sender'] == "Spiderman" else batman_avatar).write(entry['message'])

if user_input and not st.session_state.stop_chat:
    i = 0
    while i <= 5:
        user_input = interact(user_input, 'spiderman')
        
        if st.session_state.stop_chat:
            break
        time.sleep(8)
        user_input = interact(user_input, 'batman')
        
        if st.session_state.stop_chat:
            break
        time.sleep(8)
        i += 1

if st.session_state.stop_chat:
    st.write("Chat stopped by the moderator.")
