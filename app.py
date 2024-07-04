import streamlit as st

st.set_page_config(layout="wide", page_title="EduGenius", page_icon=":material/neurology:")

with st.sidebar:
    st.header("EduGenius 🧠", divider = "red")
    st.container(border=True).write("💡Got stuck? Try new Math Solver")

dashboard_page = st.Page("dashboard.py", title = "Dashboard", icon =":material/dashboard:", default=True)
math_solver = st.Page("math_solver.py", title = "Math Solver", icon =":material/function:")
research_helper = st.Page("research_helper.py", title = "Research Helper", icon =":material/insights:")
contactus_page = st.Page("contact_us.py", title = "Contact Us", icon =":material/call:")
feedback_page = st.Page("feedbacks.py", title = "Feedback", icon =":material/feedback:")
pg = st.navigation({
    "Main Menu":[dashboard_page, contactus_page, feedback_page],
    "Tools":[math_solver, research_helper]
})

pg.run()