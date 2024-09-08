import streamlit as st
import json
import os
import PIL.Image
from langchain_google_genai import GoogleGenerativeAI
from pages.canvas import free_draw, save_drawing
from output_gen import read_image, db_search, generate_answer, generate_hints, answer_gen_call, hint_gen_call, flash_model, pro_model
from utils.createVDB.create_db import embeddings
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context
from pages.math_solver import get_wolframalpha_response

from ocr.ocr import ocr_for_answer
load_dotenv()

GEMINI_PRO_API_KEY = os.getenv("GEMINI_PRO_API_KEY")

os.environ['GOOGLE_API_KEY'] = GEMINI_PRO_API_KEY
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
        
        paper_files, paper_options = get_files_without_extension(os.path.join('assets/data'))
        selected_paper_display = st.selectbox("Select a paper", paper_options)
        
        if selected_paper_display:
            selected_paper = paper_files[paper_options.index(selected_paper_display)]
            question_files, question_options = get_files_without_extension(os.path.join('assets/data', selected_paper))
            selected_question_display = st.selectbox("Select a question", question_options)
            
            if selected_question_display:
                selected_question = question_files[question_options.index(selected_question_display)]
                st.image(os.path.join('assets/data', selected_paper, selected_question))

            # Incase there were previous question stored in th session we need to remove the data associated with that 
            # specific question. Else we can just add the selected question
            if st.session_state["question"] is not None:
                st.session_state["question"] = {"paper": selected_paper, "question":selected_question_display }
                st.session_state["hints"] = []
                st.session_state["answer"] = None
                st.session_state["answer_image"] = None
                st.session_state["messages"] = []
                st.session_state["marks"] = None
                st.session_state["similar_problems"] = None
                st.session_state["improvement"] = None
                st.session_state["explanations"] = None
            else:
                st.session_state["question"] = {"paper": selected_paper, "question":selected_question_display }


        col3, col4 = st.columns(2)
        
        with col3:
            if(st.button("Want a hint?🤓", type='primary', use_container_width=True)):
                with col1:
                    with st.status("Let's see how we can help you...", expanded=True) as status:
                        response1 = generate_hints(selected_paper, selected_question, pro_model)
                        langfuse_call = hint_gen_call(pro_model, selected_question, selected_paper, response1)
                        status.update(label="Here what we found for you!",state="complete", expanded=False)

                    response_text = response1.text[7:-3]
                    hint_text = response_text
                    
                    try:
                        json_object1 = json.loads(response_text)
                        for key, value in json_object1.items():
                            title = value.get('title')
                            content = value.get('content')

                            # Append the hints conetent to the session
                            st.session_state["hints"].append(content)

                            expander = st.expander(f"{title}", icon=":material/add_circle:")
                            expander.markdown(f"##### {title}")
                            expander.markdown(content, unsafe_allow_html=True) 
                    except json.JSONDecodeError:
                        st.write(":red[Oh no! An internal error occurred😓 Please try again.]")
                    except Exception as e:
                        st.write(f":red[Oh no! An unexpected error occurred: {str(e)}]")
                    
            
            
        with col4:   
            # st.button("It is worth giving it a try💡", use_container_width=True)
            if st.button("Ask from MathSolver",use_container_width=True):
                st.switch_page("pages/math_solver.py")
                
        with col2:
            uploaded_file = st.file_uploader("Upload your answer. Let's see how you did!", type=['png', 'jpg', 'jpeg'])
            if uploaded_file is not None:
                with open(os.path.join('uploads', uploaded_file.name), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                file_path = os.path.join('assets/uploads', uploaded_file.name)
                image = PIL.Image.open(uploaded_file)
                st.image(image, use_column_width=True)
                selected_file = os.path.join('assets/uploads', uploaded_file.name)
                
            else:
                st.caption("Don't have a piece of paper? Write here!📝")
                selected_file = save_drawing(free_draw())

            
        with col2:
            @observe()
            def initialize_generation_pipeline():
                scanned_question = read_image(os.path.join('assets/data', selected_paper, selected_question), flash_model)
                        
                status.update(label="Fetching marking scheme...",state="running", expanded=False)
                context = db_search(scanned_question, llm, embeddings, 'vectorstore_2018_OL')

                status.update(label="Marking your answer...",state="running", expanded=False)
                response = generate_answer(selected_paper, selected_question, selected_file, context, pro_model)
                
                langfuse_call = answer_gen_call(pro_model, scanned_question, selected_question, selected_file, response)
                
                trace_id = langfuse_context.get_current_trace_id()
                st.session_state.trace_id = trace_id
                
                return response
            
            if st.button("Proceed", type='primary', use_container_width=True):
                 
                    st.session_state["answer_image"] = selected_file
                    st.session_state["answer"] = ocr_for_answer(selected_file)   
                # print(os.path.join('data', selected_paper, selected_question), selected_file)
                    with st.status("Analyzing question...", expanded=True) as status:
                        # scanned_question = read_image(os.path.join('assets/data', selected_paper, selected_question), flash_model)
                        
                        # status.update(label="Fetching marking scheme...",state="running", expanded=False)
                        # context = db_search(scanned_question, llm, embeddings, 'vectorstore_2018_OL')

                        # status.update(label="Marking your answer...",state="running", expanded=False)
                        # response = generate_answer(selected_paper, selected_question, selected_file, context, pro_model)
                        
                        # langfuse_call = answer_gen_call(pro_model, scanned_question, selected_question, selected_file, response)
                        response = initialize_generation_pipeline()
                        response_text = response.text[7:-3]
                        # st.write(response_text)
                        json_object = json.loads(response_text)
                        
                        status.update(label="Done. Marked your answer!",state="complete", expanded=False)



                # try:
                    
                # except:
                #     st.subheader(":red[Oh no! An internal error occured😓 Please try again.]")
        # with col1:
        #     st.page_link("pages/math_solver.py", label="\nGot stuck? Need a help?\nAsk EduGenius🧠!", icon=":material/neurology:",use_container_width=True)
                

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
    # col1, col2, col3, col4 = st.columns(4)
    # with col1:
    #     if st.button(f"👍 Like", use_container_width=True):
    #         #do something
    #         st.write("Thank you for your feedback!🌟")
    # with col2:
    #     if st.button(f"👎 Dislike", use_container_width=True):
    #         st.write("Thank you for your feedback!🌟")
    #         #do something

    # feedback_text = st.text_input("Submit Feedback:")
    # if st.button("Submit Feedback"):
    #     print(feedback_text)

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

                    if title == "Marks":
                        st.session_state["marks"] = content
                 
            st.page_link("pages/chat.py", label="\nGot doubts? Clarify them here", icon=":material/question_answer:",use_container_width=True)          
            #TODO: Seems like cannot implement the chatbot in the same page. Need to check       
            # messages = st.container(height=350)
            # prompt = st.chat_input("Ask your math question here")
            # if prompt:
            #     response = get_wolframalpha_response(prompt)
            #     markdown_text = ""
            #     for pod in response["pods"]:
                    
            #         has_content = False
            #         for subpod in pod["subpods"]:
            #             if "mathml" in subpod:
            #                 has_content = True
            #         if has_content:
            #             markdown_text += f"###### {pod['title']}\n\n"
            #             for subpod in pod["subpods"]:
            #                 if "mathml" in subpod:
            #                     markdown_text += f"\n{subpod['mathml']}\n\n"
            #         has_content = False
                            
            #     messages.chat_message("user").markdown(prompt, unsafe_allow_html=True)
            #     messages.chat_message("assistant").markdown(f"##### Result:\n\n{markdown_text}", unsafe_allow_html=True)
        
        with col4:
            for i, (key, value) in enumerate(json_object.items()):
                if i >= 2:
                    title = value.get('title')
                    content = value.get('content')
                    expander = st.expander(f"{title}", icon=":material/add_circle:")
                    expander.markdown(f"##### {title}")
                    expander.markdown(f"{content}", unsafe_allow_html=True) 

                    if title == "Explanation":
                        st.session_state["explanation"] = content
                    elif title == "Improvement":
                        st.session_state["improvement"] = content
                    elif title == "Similar Problems":
                        st.session_state["similar_problems"] = content
                    

            # for i in st.session_state:
                # print(i, st.session_state[i])
            
            st.page_link("pages/feedbacks.py", label="\nWe appreciate your rating. Please rate this session here!", icon=":material/reviews:",use_container_width=True) 
    except:
        st.markdown("##### Results will be displayed here📝")
        st.caption("Please do not forget to rate the answer!🌟")
else:
    st.header("You need to login to access this :red[_feature_]🔒")
    st.page_link("pages/home.py", label="Click here to login", icon=":material/lock_open:", use_container_width=True)
