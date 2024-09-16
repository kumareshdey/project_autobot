import time
import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler


model1 = OllamaLLM(model="llama3.1:8b", temperature=1, callbacks=[])
model2 = OllamaLLM(model="llama3.1:8b", temperature=1, callbacks=[])

template1 = "You are funny avenger hero spiderman. Can you please answer based on this reply: {ctx}? Also ask me follow up questions to keep the conversation live. Keep it short like whatsapp."
prompt1 = ChatPromptTemplate.from_template(template=template1)
chain1 = prompt1 | model1

template2 = "You are funny disney hero batman. Can you please answer based on this reply: {ctx}? Also ask me follow up questions to keep the conversation live. Keep it short like whatsapp."
prompt2 = ChatPromptTemplate.from_template(template=template2)
chain2 = prompt2 | model2

siri_style = """
<div style='background-color: #f0f8ff; padding: 10px; border-radius: 10px; margin: 10px 0;'>
    <strong style='color: #007AFF;'>Spiderman:</strong>
    <p style='color: #000000;'>{}</p>
</div>
"""

alexa_style = """
<div style='background-color: #e6ffe6; padding: 10px; border-radius: 10px; margin: 10px 0;'>
    <strong style='color: #34A853;'>Batman:</strong>
    <p style='color: #000000;'>{}</p>
</div>
"""

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'stop_chat' not in st.session_state:
    st.session_state['stop_chat'] = False

ctx_input = st.text_input('Enter the starting context:', '')

start_chat = st.button('Start Chat')
stop_chat = st.button('Stop Chat')

if stop_chat:
    st.session_state['stop_chat'] = True

chat_container = st.empty()

if start_chat and ctx_input:
    st.session_state['stop_chat'] = False 
    ctx = ctx_input 

    while not st.session_state['stop_chat']:
        ctx = chain1.invoke(ctx)

        st.session_state['chat_history'].append(siri_style.format(ctx))
        
        chat_display = '\n'.join(st.session_state['chat_history'])
        with chat_container.container():
            st.markdown(
                f"<div id='chat-container' style='max-height: 400px; overflow-y: auto;'>{chat_display}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<script>document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;</script>",
                unsafe_allow_html=True
            )

        time.sleep(4)
        ctx = chain2.invoke(ctx)
        st.session_state['chat_history'].append(alexa_style.format(ctx))
        chat_display = '\n'.join(st.session_state['chat_history'])
        with chat_container.container():
            st.markdown(
                f"<div id='chat-container' style='max-height: 400px; overflow-y: auto;'>{chat_display}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<script>document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;</script>",
                unsafe_allow_html=True
            )
        
        time.sleep(4)

else:
    st.write("Enter a valid starting context and click 'Start Chat' to begin the conversation.")
