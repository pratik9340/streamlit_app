from huggingface_hub import InferenceClient
import streamlit as st

from dotenv import load_dotenv
load_dotenv() #Importing all the environment variables
from PIL import Image
import os 

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_TOKEN"),)

def clent_transformer(t):
  completion = client.chat.completions.create(
      model="HuggingFaceH4/zephyr-7b-beta",
      messages=[
          {
              "role": "user",
              "content": t
          }
      ],
  )
  return completion.choices[0].message.content


st.set_page_config(page_title= "Chatbot HF")
st.header("Chatbot with model zephyr-7b-beta from Hugging face")

#Initializing session state for chat history if it does not exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:", key = 'input')
submit = st.button("Ask")

if submit and input:
    response = clent_transformer(input)
    #Adding our queries to chat history
    st.session_state['chat_history'].append(("You:", input))
    st.subheader("Response:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot:", chunk.text))
st.subheader("Conversation")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")