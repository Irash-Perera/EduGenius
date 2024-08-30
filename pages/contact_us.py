import streamlit as st
from streamlit_card import card

st.header("Feel free to reach out to :red[_us_]! 📧", divider = "red")

col1, col2, col3 = st.columns(3)

with col1:
    hasClicked = card(
        title = "Irash Perera",
        text= "irash.21@cse.mrt.ac.lk",
        image = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F792070653234421442%2F&psig=AOvVaw1VbTRqt-u20J4ypnXK-PSu&ust=1720383976393000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCNDt-vKfk4cDFQAAAAAdAAAAABAE",
        url = "https://github.com/Irash-Perera"
    )

with col2:
    hasClicked = card(
        title = "Hansana Prabashwara",
        text= "hansana.21@cse.mrt.ac.lk",
        image = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F792070653234421442%2F&psig=AOvVaw1VbTRqt-u20J4ypnXK-PSu&ust=1720383976393000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCNDt-vKfk4cDFQAAAAAdAAAAABAE",
        url = "https://github.com/HansanaPrabashwara-210483T"
    )

with col3:
    hasClicked = card(
        title = "Pranavan Subendiran",
        text= "subendiran.21@cse.mrt.ac.lk",
        image = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F792070653234421442%2F&psig=AOvVaw1VbTRqt-u20J4ypnXK-PSu&ust=1720383976393000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCNDt-vKfk4cDFQAAAAAdAAAAABAE",
        url = "https://github.com/Pranavan-S"
    )