import streamlit as st
from core.qa_chat import respond_for_user_question
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAI



load_dotenv()

GEMINI_PRO_API_KEY = os.getenv("GEMINI_PRO_API_KEY")

os.environ['GOOGLE_API_KEY'] = GEMINI_PRO_API_KEY
llm = GoogleGenerativeAI(model = "gemini-pro", temperature=0.7)

st.header("Got any :red[_doubts_]🤔? Ask me anything!", divider="red")

if st.session_state["authentication_status"]:

    # :TODO Add a if clause to make the chat available only when the answer was given by the user

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input("Ask questions to clarify any doubts")

    if user_question:
        with st.chat_message("user"):
            st.write(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})
        respond_for_user_question(user_question,llm)        
else:
    st.header("You need to login to access this :red[_feature_]🔒")
    st.page_link("pages/home.py", label="Click here to login", icon=":material/lock_open:", use_container_width=True)
