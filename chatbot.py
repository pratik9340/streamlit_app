from dotenv import load_dotenv
load_dotenv() #Importing all the environment variables
from PIL import Image

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Creating a function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream= True)
    return response

# Initializing streamlit app
st.set_page_config(page_title= "Q&A Demo")
st.header("Chatbot")

#Initializing session state for chat history if it does not exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:", key = 'input')
submit = st.button("Ask")

if submit and input:
    response = get_gemini_response(input)
    #Adding our queries to chat history
    st.session_state['chat_history'].append(("You:", input))
    st.subheader("Response:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot:", chunk.text))
st.subheader("Conversation")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
