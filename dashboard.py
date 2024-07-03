import streamlit as st
import os
from PIL import Image
from canvas import free_draw, save_drawing

st.header("Welcome to EduGenius 🧠", divider= 'red')

col1, col2 = st.columns(2)

def get_files_without_extension(directory):
    files = os.listdir(directory)
    files_without_extension = [os.path.splitext(file)[0] for file in files]
    return files, files_without_extension


with col1:
    paper_files, paper_options = get_files_without_extension(os.path.join('data'))
    selected_paper_display = st.selectbox("Select a paper", paper_options)
    
    if selected_paper_display:
        selected_paper = paper_files[paper_options.index(selected_paper_display)]
        question_files, question_options = get_files_without_extension(os.path.join('data', selected_paper))
        selected_question_display = st.selectbox("Select a question", question_options)
        
        if selected_question_display:
            selected_question = question_files[question_options.index(selected_question_display)]
            st.image(os.path.join('data', selected_paper, selected_question))

    col3, col4 = st.columns(2)
    
    with col3:
        st.button("Show Answer", type='primary', use_container_width=True)
    with col4:   
        st.button("It is worth giving it a try💡", use_container_width=True)
        
          
    with col2:
        uploaded_file = st.file_uploader("Upload your answer. Let's see how you did!", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            with open(os.path.join('uploads', uploaded_file.name), 'wb') as f:
                f.write(uploaded_file.getbuffer())
            file_path = os.path.join('uploads', uploaded_file.name)
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            
            selected_file = os.path.join('uploads', uploaded_file.name)
        else:
            st.caption("Don't have a piece of paper? Write here!📝")
            selected_file = save_drawing(free_draw())
        print(selected_file)
      
            
        
        
            
                    
                


                