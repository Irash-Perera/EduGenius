import streamlit as st
from streamlit_card import card

st.title("Contact Us")

col1, col2, col3 = st.columns(3)

with col1:
    hasClicked = card(
        title = "Irash Perera",
        text= "irash.21@cse.mrt.ac.lk",
        image = "https://avatars.githubusercontent.com/u/42272743?s=400&u=d32d37496c143c06050c330053848ffbf556d42f&v=4",
        url = "https://github.com/Irash-Perera"
    )