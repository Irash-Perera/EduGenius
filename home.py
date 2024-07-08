import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit.components.v1 as components
import datetime
import json 
import requests  
from streamlit_lottie import st_lottie 

from auth.hasher import Hasher
from auth.authenticate import Authenticate
from auth.db import collection

# Animation
url = requests.get( 
    "https://lottie.host/db543e89-2136-494d-985a-aab7aa9eb038/Hd6mwuZ6d2.json") 
url_json = dict() 
if url.status_code == 200: 
    url_json = url.json() 
else: 
    print("Error in the animation URL") 

# Loading config file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
# if 'authentication_status' not in st.session_state:
#     st.session_state['authentication_status'] = None
# if 'name' not in st.session_state:
#     st.session_state['name'] = ''
# if 'email' not in st.session_state:
#     st.session_state['email'] = ''

# Creating the authenticator object
authenticator = Authenticate(
    collection,
    config['cookie']['name'], 
    config['cookie']['key'], 
    config['cookie']['expiry_days'],
)


def greeting():
    currentTime = datetime.datetime.now()
    if currentTime.hour < 12:
        return ('Good morning,')
    elif 12 <= currentTime.hour < 18:
        return ('Good afternoon,')
    else:
        return ('Good evening,')

st.header("Edu:red[Genius] 🧠", divider = "red")

col1, col2 = st.columns(2)
with col1:
    st.subheader("What is EduGenius❓", divider = "gray")
    st.markdown("""

In modern education, personalized and efficient tutoring remains a challenge, particularly in mathematics. Traditional tutoring methods often lack flexibility and efficiency, hindering the learning process.""")
 
    st.subheader("Our Mission 🎯", divider = "gray")

    st.markdown("""EduGenius aims to provide a personalized and efficient AI-powered tutoring system for A/Level and O/Level students in mathematics.""") 

    st.subheader("Key Features 🚀", divider = "gray")
    st.markdown("""
    - **Personalized Tutoring Materials**: Utilizes pre-processed and pre-stored maths marking schemes in the vector database.
    - **Advanced Technologies**: Leverages the latest technologies like LangChain, Wolfram, and Gemini.
    - **Interactive and Personalized**: Generates interactive and personalized tutoring materials for students.
    - **Real-Time Evaluation**: Evaluates student performance in real-time.
    - **Instant Feedback**: Provides instant, accurate feedback and grades.
    - **Enhanced Learning Experience**: Enhances the learning experience, supporting students in their learning journey.

    Explore EduGenius and transform your learning experience in mathematics!""")

with col2:
    authenticator.login('Login', 'main')
    if st.session_state["authentication_status"]:
        st.subheader(f'{greeting()} :red[_{st.session_state["name"]}_]')
        authenticator.logout('Logout', 'main')
        st_lottie(url_json) 
        
    elif st.session_state["authentication_status"] is None and st.session_state["FormSubmitter:Login-Login"]:
        st.error('Username/password is incorrect' , icon = ":material/sentiment_very_dissatisfied:")
        
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password', icon=":material/lock_open:")
        
    # st.write(st.session_state)
        
    if st.session_state["authentication_status"] is None:
        st.markdown("#### Create a new account here 👇")
        try:
            if authenticator.register_user('Register user'):
                st.success('User registered successfully. Try logging in now.', icon=':material/sentiment_satisfied:')
        except Exception as e:
            st.error(e)
            
        print(st.session_state["authentication_status"])
    
    # # Creating a forgot password widget
    # try:
    #     username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password?')
    #     if username_forgot_pw:
    #         st.success('New password sent securely')
    #         st.write(username_forgot_pw)
    #         st.write(email_forgot_password)
    #         st.write(random_password)
    
    #         # Random password to be transferred to user securely
    #     else:
    #         st.error('Username not found')
    # except Exception as e:
    #     st.error(e)

    # # Creating a forgot username widget
    # try:
    #     username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
    #     if username_forgot_username:
    #         st.success('Username sent securely')
    #         # Username to be transferred to user securely
    #     else:
    #         st.error('Email not found')
    # except Exception as e:
    #     st.error(e)