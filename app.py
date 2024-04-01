import streamlit as st
from llm_chain import normal_chain
from langchain.memory import StreamlitChatMessageHistory
from utils import save_chat_history_json
import yaml
import os

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def load_chain(chat_history):
    return normal_chain(chat_history)

def save_chat_history():
    # If there is a chat history to save, save it
    if 'history' in st.session_state and st.session_state.history:
        file_path = os.path.join(config["chat_history_path"], "random.json")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save the chat history
        save_chat_history_json(st.session_state.history, file_path)



def main():

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'user_question' not in st.session_state:
        st.session_state.user_question = ""
    if 'send_input' not in st.session_state:
        st.session_state.send_input = False

    st.title("Product Tracking Chatbot")
    chat_container = st.container()
    st.sidebar.title("Chat Sessions")

    chat_sessions = ["new_session"] + os.listdir(config['chat_history_path'])

    st.sidebar.selectbox("Select a Chat session", chat_sessions, key="session_key")
    
    chat_history = StreamlitChatMessageHistory()
    llm_chain = load_chain(chat_history)


    user_input = st.text_input("Type your message here", key="user_input")
    send_button = st.button("Send", key="send_button", on_click=process_input)


    if st.session_state.user_question:
        with chat_container:
            st.write(f"User: {st.session_state.user_question}")

            llm_response = llm_chain.run(st.session_state.user_question)
            st.write(f"AI: {llm_response}")

    if chat_history.messages != []:
        with chat_container:
            st.write("Chat History:")
            for message in chat_history.messages:
                st.chat_message(message.type).write(message.content)

    save_chat_history()
def process_input():

    chat_history = StreamlitChatMessageHistory()
    llm_chain = load_chain(chat_history)
    # Assuming that 'user_question' is the user's input text
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""
    
    # Process the user input and get the AI response
    ai_response = llm_chain.run(st.session_state.user_question)

    # Directly create dictionaries for user and AI messages
    user_message = {"type": "human", "content": st.session_state.user_question}
    ai_message = {"type": "ai", "content": ai_response}

    # Append the new messages to the history
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.extend([user_message, ai_message])


if __name__ == '__main__':
    main()
