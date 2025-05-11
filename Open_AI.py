import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import streamlit as st

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") )# Reads from .env file

def OPEN_AI(input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4-turbo" or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful chatbot"},
                {"role": "user", "content": input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


chat = client.start_chat(history=[])


# Initializing streamlit app
st.set_page_config(page_title= "Q&A Demo")
st.header("Chatbot")

#Initializing session state for chat history if it does not exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:", key = 'input')
submit = st.button("Ask")

if submit and input:
    response = OPEN_AI(input)
    #Adding our queries to chat history
    st.session_state['chat_history'].append(("You:", input))
    st.subheader("Response:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot:", chunk.text))
st.subheader("Conversation")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
