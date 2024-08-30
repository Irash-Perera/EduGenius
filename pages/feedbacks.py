import streamlit as st
from langfuse import Langfuse
st.header("Give us your :red[feedback]", divider= "red")

st.markdown("##### We would love to hear your feedback on the question you just attempted. Your feedback will help us improve our services.")
st.write(":red[Note!] You can submit your feedbacks for each attempt.")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("##### How's your current session?")
    
with col2:
  sentiment_mapping = ["one", "two", "three", "four", "five"]
  selected = st.feedback("stars")
  rating = 3
  if selected is not None:
    rating = selected+1
  
  comment = st.text_area("Any comments?(optional)","", height=100)

    
langfuse_client = Langfuse()

with col2:
  if st.button("Submit feedback", type='primary', use_container_width=True):
    langfuse_client.score(
        trace_id=st.session_state.trace_id,
        name="user-explicit-feedback",
        value=rating,
        comment=comment
    )

