import streamlit as st
import json
import os
import PIL.Image
from langchain_google_genai import GoogleGenerativeAI
from canvas import free_draw, save_drawing
from output_gen import read_image, db_search, generate_answer
from create_db import embeddings
from env import API_KEY


os.environ['GOOGLE_API_KEY'] = API_KEY
llm = GoogleGenerativeAI(model = "gemini-pro", temperature=0.7)

def get_files_without_extension(directory):
    files = os.listdir(directory)
    files_without_extension = [os.path.splitext(file)[0] for file in files]
    return files, files_without_extension

st.header("Welcome to EduGenius 🧠", divider= 'red')


if st.session_state["authentication_status"]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Let's get started!🚀")
        
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
                image = PIL.Image.open(uploaded_file)
                st.image(image, use_column_width=True)
                selected_file = os.path.join('uploads', uploaded_file.name)
                
            else:
                st.caption("Don't have a piece of paper? Write here!📝")
                selected_file = save_drawing(free_draw())
            
        with col2:
            if st.button("Proceed", type='primary', use_container_width=True):
                try:
                    # print(os.path.join('data', selected_paper, selected_question), selected_file)
                    with st.status("Analyzing question...", expanded=True) as status:
                        scanned_question = read_image(os.path.join('data', selected_paper, selected_question))
                        
                        status.update(label="Fetching marking scheme...",state="running", expanded=False)
                        context = db_search(scanned_question, llm, embeddings, 'vectorstore_2018_OL')

                        status.update(label="Marking your answer...",state="running", expanded=False)
                        response = generate_answer(selected_paper, selected_question, selected_file, context)
                        response_text = response.text[7:-3]
                        json_object = json.loads(response_text)
                        
                        status.update(label="Done. Marked your answer!",state="complete", expanded=False)
                except:
                    st.subheader(":red[Oh no! An internal error occured😓 Please try again.]")
        with col1:
            st.page_link("math_solver.py", label="\nGot stuck? Need a help?\nAsk EduGenius🧠!", icon=":material/neurology:",use_container_width=True)
                

    #================================================================================
    #                            Results Section                                    |
    #================================================================================

    # Styling for the results
    st.markdown(
        """
        <style>
        .math-content {
            font-size: 20px; /* Adjust the font size as needed */
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.subheader("Results 📝", divider="gray")
    col3, col4 = st.columns(2)
    try:
        with col3:
            for i, (key, value) in enumerate(json_object.items()):
                if i < 2:
                    title = value.get('title')
                    content = value.get('content')
                    formatted_content = f'<div class="math-content">{content}</div>'
                    st.subheader(f":green[_{title}_]")
                    st.markdown(formatted_content, unsafe_allow_html=True)
        with col4:
            for i, (key, value) in enumerate(json_object.items()):
                if i >= 2:
                    title = value.get('title')
                    content = value.get('content')
                    expander = st.expander(f"{title}", icon=":material/add_circle:")
                    expander.markdown(f"##### {title}")
                    expander.markdown(f"{content}", unsafe_allow_html=True) 
        
    except:
        st.markdown("##### Results will be displayed here📝")
else:
    st.header("You need to login to access this :red[_feature_]🔒")
    st.page_link("home.py", label="Click here to login", icon=":material/lock_open:", use_container_width=True)
