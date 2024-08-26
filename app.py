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



home_page = st.Page("page/home.py", title = "Home", icon =":material/home:", default=True)
dashboard_page = st.Page("page/dashboard.py", title = "Dashboard", icon =":material/dashboard:")
math_solver = st.Page("page/math_solver.py", title = "Math Solver", icon =":material/function:")
# research_helper = st.Page("research_helper.py", title = "Research Helper", icon =":material/insights:")
contactus_page = st.Page("page/contact_us.py", title = "Contact Us", icon =":material/call:")
feedback_page = st.Page("page/feedbacks.py", title = "Feedback", icon =":material/feedback:")
pg = st.navigation({
    "Main Menu":[home_page, dashboard_page, math_solver, contactus_page, feedback_page]
})

pg.run()