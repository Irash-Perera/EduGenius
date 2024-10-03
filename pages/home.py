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

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col4:
    style_image1 = """
                    width: 50%;
                    height: auto;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: -20px;
                    """
    st.markdown(
        f'<div style="display: flex; justify-content: center; align-items: center;"><img src="{"./app/static/edugenius_icon.png"}" style="{style_image1}"></div>',
        unsafe_allow_html=True,
    )
    # st.image("assets/brand/edugenius_icon.png", use_column_width=True)
    
st.html("""
    <div class="container">
        <h5 class="title">EduGenius</h5>
        <h2>Learn Smater. Get Personalized Help.</h2> 
    </div>
""")

login, register = st.tabs(["Login", "Register"])
tabstyle = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.2rem;
    }
</style>
'''
st.markdown(tabstyle, unsafe_allow_html=True)

with login:
    authenticator.login('Login', 'main')
    if st.session_state["authentication_status"]:
        st.subheader(f'{greeting()} :red[{st.session_state["name"]}]👋')
        authenticator.logout('Logout', 'main') 
        
    elif st.session_state["authentication_status"] is None and st.session_state["FormSubmitter:Login-Login"]:
        st.error('Username/password is incorrect' , icon = ":material/sentiment_very_dissatisfied:")
        
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password', icon=":material/lock_open:")
        
with register:   
    if st.session_state["authentication_status"] is None:
        st.markdown("#### Create a new account here 👇")
        try:
            if authenticator.register_user('Register user'):
                st.success('User registered successfully. Try logging in now.', icon=':material/sentiment_satisfied:')
        except Exception as e:
            st.error(e)
    else:
        st.error('You are already logged in. Please logout to register a new account.')
        
        # print(st.session_state["authentication_status"])
    
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