import streamlit as st

fav_icon = "assets/brand/edugenius_icon.png"
st.set_page_config(layout="wide", page_title="EduGenius", page_icon=fav_icon)

st.html("""
  <style>
    [alt=Logo] {
      height: 3rem;
    }
  </style>
        """)

sidear_logo = "assets/brand/edugenius_logo.png"
main_body_logo = "assets/brand/edugenius_icon.png"

st.logo(sidear_logo, icon_image=main_body_logo)



home_page = st.Page("pages/home.py", title = "Home", icon =":material/home:", default=True)
dashboard_page = st.Page("pages/dashboard.py", title = "Dashboard", icon =":material/dashboard:")
QA = st.Page("pages/chat.py", title = "Q&A", icon =":material/question_answer:")
math_solver = st.Page("pages/math_solver.py", title = "Math Solver", icon =":material/function:")
contactus_page = st.Page("pages/contact_us.py", title = "Contact Us", icon =":material/call:")
feedback_page = st.Page("pages/feedbacks.py", title = "Feedback", icon =":material/feedback:")
documentation_page = st.Page("pages/documentation.py", title = "Documentation", icon =":material/book:")
test_page = st.Page("pages/test.py", title = "Test", icon =":material/assessment:")
pg = st.navigation({
    "Main Menu":[home_page, dashboard_page,QA, math_solver, contactus_page, feedback_page, documentation_page]
})

with st.sidebar:
    st.write("Admin Tools")
    st.link_button("Admin Dashboard", 'https://cloud.langfuse.com/project/clyejfzen000vootvl9vdtb7g', use_container_width=True)

pg.run()