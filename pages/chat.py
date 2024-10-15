import streamlit as st
from core.qa_chat import respond_for_user_question
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAI
from auth.authenticate import Authenticate
from auth.db import collection
import yaml

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = Authenticate(
    collection,
    config['cookie']['name'], 
    config['cookie']['key'], 
    config['cookie']['expiry_days'],
)
authenticator._check_cookie()


load_dotenv()

GEMINI_PRO_API_KEY = os.getenv("GEMINI_PRO_API_KEY")

os.environ['GOOGLE_API_KEY'] = GEMINI_PRO_API_KEY
llm = GoogleGenerativeAI(model = "gemini-pro", temperature=0.7)



def flush_messages():
    st.session_state.messages = []

def flush_context():
    st.session_state["question"] = None
    st.session_state["question_text"] = None
    st.session_state["hints"] = []
    st.session_state["answer"] = None
    st.session_state["answer_image"] = None
    # st.session_state["messages"] = []
    st.session_state["marks"] = None
    st.session_state["similar_problems"] = None
    st.session_state["improvement"] = None
    st.session_state["explanation"] = None
    
st.header("Got any :red[_doubts_]🤔? Ask me anything!", divider="red")

# st.write(st.session_state)
with st.sidebar:
    st.info("Make sure to flush the context before trying a new question in the dashboard.", icon=":material/info:")
if st.session_state["authentication_status"]:
    # :TODO Add a if clause to make the chat available only when the answer was given by the user
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.question_text != None:
        col1,space,col2 = st.columns((6,6,3))

        with col1:
            st.markdown("##### " +st.session_state.question["paper"]+" / "+st.session_state.question["question"], unsafe_allow_html=True)
        
        with col2:
            if st.session_state.marks != None:
                st.markdown("##### "+":green[Gained Marks]: " +st.session_state.marks, unsafe_allow_html=True)

        question_expander = st.expander("Question", icon=":material/add_circle:")
        # question_expander.markdown(f"##### Question")
        question_expander.markdown(st.session_state.question_text, unsafe_allow_html=True) 

        answer_expander = st.expander("Provided Answer", icon=":material/add_circle:")
        answer_expander.markdown(st.session_state.answer, unsafe_allow_html=True)

        explanation_expander = st.expander("Explanation", icon=":material/add_circle:")
        explanation_expander.markdown(st.session_state.explanation, unsafe_allow_html=True)

        if st.session_state.improvement != None:
            improvements_expander = st.expander("Improvements", icon=":material/add_circle:")
            improvements_expander.markdown(st.session_state.improvement, unsafe_allow_html=True)
        
        if st.session_state.marking_scheme != None:
            ms_expander = st.expander("Marking Scheme", icon=":material/add_circle:")
            ms_expander.markdown(st.session_state.marking_scheme["answer"], unsafe_allow_html=True)

        if st.session_state.similar_problems != None:
            sps_expander = st.expander("Similar Problems", icon=":material/add_circle:")
            sps_expander.markdown(st.session_state.similar_problems, unsafe_allow_html=True)

        if st.session_state.hints != None and len(st.session_state.hints) != 0:
            hints_expander = st.expander("Hints", icon=":material/add_circle:")
            hints_expander.markdown(st.session_state.hints, unsafe_allow_html=True)

    if st.session_state.messages != [] and st.session_state.question_text != None:
        st.divider()



    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    user_question = st.chat_input("Ask questions to clarify any doubts")

    if user_question:
        with st.chat_message("user"):
            st.write(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})
        respond_for_user_question(user_question,llm)  



    # if st.session_state.messages != []:
    #     col1, col2, col3 = st.columns(3)
    #     with col2:
    #         st.button("Clear Chat",on_click=flush_messages, use_container_width=True)
    
      
    if st.session_state.question_text != None:
        # st.divider()
        st.markdown('###') 
        if st.session_state.messages == []:
            col1, col2, col3 = st.columns(3)
            with col2:
                st.button("Clear Context",on_click=flush_context,use_container_width=True, icon=":material/delete:")
        else:
            col1, col2, col3, col4 = st.columns(4)
            with col2:
                st.button("Clear Chat",on_click=flush_messages,use_container_width=True, icon=":material/delete_forever:")
            with col3:
                st.button("Clear Context",on_click=flush_context,use_container_width=True, type="primary", icon=":material/delete_forever:")
    else:
        if st.session_state.messages != []:
            # st.divider()
            st.markdown('###') 
            col1, col2, col3 = st.columns(3)
            with col2:
                st.button("Clear Chat",on_click=flush_messages,use_container_width=True, type="primary", icon=":material/delete_forever:")   
else:
    st.header("You need to login to access this :red[_feature_]🔒")
    st.page_link("pages/home.py", label="Click here to login", icon=":material/lock_open:", use_container_width=True)
