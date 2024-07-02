import streamlit as st

st.set_page_config(layout="wide", page_title="EduGenius", page_icon=":material/neurology:")

with st.sidebar:
    st.title("EduGenius 🧠")
    st.caption("Your Personal AI Tutor", )

dashboard_page = st.Page("dashboard.py", title = "Dashboard", icon =":material/dashboard:", default=True)
contactus_page = st.Page("contact_us.py", title = "Contact Us", icon =":material/call:")
feedback_page = st.Page("feedbacks.py", title = "Feedback", icon =":material/feedback:")
pg = st.navigation([dashboard_page, contactus_page, feedback_page])

pg.run()