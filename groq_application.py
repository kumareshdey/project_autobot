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

# Define templates for Spiderman and Batman
template1 = "You are funny avenger hero Spiderman. Can you debate with Batman based on this reply: {ctx}?  Just add one short relevant comment against the reply. Use emojis if possible."
prompt1 = ChatPromptTemplate.from_template(template=template1)

template2 = "You are funny Disney hero Batman. Can you debate with Spiderman based on this reply: {ctx}? Just add one short relevant comment against the reply. Use emojis if possible."
prompt2 = ChatPromptTemplate.from_template(template=template2)

# Chain templates to models
chain1 = prompt1 | model1
chain2 = prompt2 | model2

# Add icon URLs (replace with your own URLs if you have specific images)
spiderman_avatar = "spidy.jpg"
batman_avatar = "batty.jpeg"

st.title("Spiderman vs Batman")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You (as the moderator):", key="input")

def interact(user_message):
    # Spiderman responds
    ctx = user_message
    while ctx:
        ctx = chain1.invoke(ctx).content
        st.session_state.history.append({"sender": "Spiderman", "message": ctx})
        
        st.chat_message("Spiderman", avatar=spiderman_avatar).write(ctx)
        time.sleep(8)

        ctx = chain2.invoke(ctx).content
        st.session_state.history.append({"sender": "Batman", "message": ctx})

        st.chat_message("Batman", avatar=batman_avatar).write(ctx)
        time.sleep(8)

if user_input:
    interact(user_input)
