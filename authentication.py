import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit.components.v1 as components

from auth.hasher import Hasher
from auth.authenticate import Authenticate
from auth.db import collection

# Loading config file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = Authenticate(
    collection,
    config['cookie']['name'], 
    config['cookie']['key'], 
    config['cookie']['expiry_days'],
)

# print("Authentication object created")

try:
    if authenticator.register_user('Register user'):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)
    
# creating a login widget
authenticator.login('Login', 'main')
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')