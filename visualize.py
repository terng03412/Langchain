import streamlit as st
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

import os

# Retrieve the API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")


# Initialize the language model
llm = OpenAI(api_key=openai_api_key)

# Initialize memory
memory = ConversationBufferMemory()

# Define a conversation chain with memory
conversation_chain = ConversationChain(llm=llm, memory=memory)

# Streamlit app
st.title("LangChain Chatbot")

if "responses" not in st.session_state:
    st.session_state["responses"] = []

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

def get_response():
    user_input = st.session_state.user_input
    if user_input:
        response = conversation_chain.run(user_input)
        st.session_state.responses.append((user_input, response))
        st.session_state.user_input = ""

st.text_input("You: ", key="user_input", on_change=get_response)

for user_input, response in st.session_state.responses:
    st.write(f"User: {user_input}")
    st.write(f"Bot: {response}\n")
