import streamlit as st
from PIL import Image
import os

import google.generativeai as genai
genai.configure(api_key="AIzaSyCTgGGqLWEfxEmYr1zFf6SFPgGU8-fIN48")

model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Math Solver", page_icon="🧮", layout="wide")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Upload a photo")
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        selected_file = uploaded_file.name
        with open(os.path.join('uploaded_images', selected_file), 'wb') as f:
            f.write(uploaded_file.getbuffer())
        file_path = os.path.join('uploaded_images', selected_file)
        
        f = genai.upload_file(path = file_path)
        file = genai.get_file(name=f.name)
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', width=300)
        response = model.generate_content([f, "Describe the image. If it is about a math problem, then solve it simple way anddescribe each steps and give in latex format."])
with col2:
    #show the uploaded image
    if uploaded_file is not None:
        st.subheader("Answer")
        st.write(response.text)

        