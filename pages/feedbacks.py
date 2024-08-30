import streamlit as st
from langfuse import Langfuse
from streamlit_lottie import st_lottie 
import json 
import requests  

# Animation
url = requests.get( 
    "https://lottie.host/db543e89-2136-494d-985a-aab7aa9eb038/Hd6mwuZ6d2.json") 
url_json = dict() 
if url.status_code == 200: 
    url_json = url.json() 
else: 
    print("Error in the animation URL") 
    
st.header("Give us your :red[feedback] ✨", divider= "red")

st.markdown("##### We would love to hear your feedback on the question you just attempted. Your feedback will help us improve our services.")
st.write(":red[Note!] You can submit your feedbacks for each attempt.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("##### How's your current session?")
    st_lottie(url_json, width=250, height=250)
    
with col2:
  if st.session_state.trace_id is not None:
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")
    rating = 3
    if selected is not None:
      rating = selected+1
    
    comment = st.text_area("Any comments?(optional)","", height=100)
    langfuse_client = Langfuse()
    if st.button("Submit feedback", type='primary', use_container_width=True):
      langfuse_client.score(
          trace_id=st.session_state.trace_id,
          name="user-explicit-feedback",
          value=rating,
          comment=comment
      )
      st.session_state.trace_id = None
  else:
    with col1:
      st.markdown("###### Please :red[attempt] a question to give feedback.⛓️‍💥")
st.page_link("pages/dashboard.py", label="\nBack to learn", icon=":material/arrow_back:",use_container_width=True) 


