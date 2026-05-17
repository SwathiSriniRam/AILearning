from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq


# load environment variables from .env file
load_dotenv()

# initialize the streamlit app configuration
st.set_page_config(page_title=" Chatbot", 
                   page_icon="🤖", 
                   layout="centered")

st.title("💬 Generative AI Chatbot")

#initialize chat history
chat_history = []

# create a text input for user queries
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#show chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

#llm initialization
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.0,
)

user_input = st.chat_input("Ask Chatbot...")

#handle user input and generate response
if user_input:
    # add user message to chat history
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # generate response from the model
    response = llm.invoke(
        input=[{"role": "system", "content": "You are a helpful assistant."}, * st.session_state.chat_history]
    )

    assistant_response = response.content
    
    # add model response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    
    with st.chat_message("assistant"): 
        st.markdown(assistant_response)