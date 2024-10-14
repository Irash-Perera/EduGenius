import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
from dotenv import load_dotenv
import os
from langchain.vectorstores import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.wolfarm import get_wolframalpha_response
from utils.createVDB.create_db import embeddings


load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))




def reformat_curly_brackets(text):
    """Reformat the given text to hansle curly brackets issues in the templates

    Args:
        text (string): Text to be reformatted

    Returns:
        string: reformatted text 
    """
    if "{" in text or "}" in text:
        text = text.replace("{", "{{")
        text = text.replace("}", "}}")
    return text


def get_page_content(relevent_documents):
    """Get the page content from the given documents

    Args:
        relevent_documents (Chroma.documents): Document objects retived after similarity search

    Returns:
        string : page contents as a single string
    """
    if relevent_documents == None:
        return None
    else:
        context = ""
        for i in relevent_documents:
            context += i.page_content
            context += ",    "
        return reformat_curly_brackets(context)

#TODO: Not used
def convert_to_markdown(response):
    """Convert the response from wolframalpha to markdown format

    Args:
        response (json): wolfram response 

    Returns:
        string : reormatted markdown as a string 
    """
    markdown_text = ""
    for pod in response["pods"]:
        has_content = False
        for subpod in pod["subpods"]:
            if "mathml" in subpod:
                has_content = True
        if has_content:
            markdown_text += f"###### {pod['title']}\n\n"
            for subpod in pod["subpods"]:
                if "mathml" in subpod:
                    markdown_text += f"\n{subpod['mathml']}\n\n"
    return reformat_curly_brackets(markdown_text)



def QA_RAG(query,llm,vs1_path,vs2_path,k,threshold,session = None):

    # Textbook Vector Store data rerical
    vector_textbook = Chroma(persist_directory=vs1_path, embedding_function=embeddings)
    textbook_retriver = vector_textbook.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'score_threshold': threshold}
    )
    relevent_textbook_documents = textbook_retriver.get_relevant_documents(query)
    relevent_textbook_content = get_page_content(relevent_textbook_documents)

    # Questions vectorstore data retival chain
    vectordb = Chroma(persist_directory=vs2_path, embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": k})

    # Get session data
    question_str = ''
    answer_str = ''
    explanations_str = ''
    marks_str = ''
    similar_problems_str = ''
    improvements_str = ''
    hints_str = ''
    history = ''
    
    ## Chat History
    if session != None:
        history = "history: "
        for message in session["messages"]:
            history += reformat_curly_brackets(message["content"]) + " "

        question = session["question_text"]
        answer = session["answer"]
        explanations = session["explanation"]
        marks = session["marks"]
        similar_problems = session["similar_problems"]
        improvements = session["improvement"]
        hints = session["hints"]
        
        if question != None:
            question_str = f"question : {reformat_curly_brackets(question)}"

        if answer != None:
            answer_str = f"provided answer : {reformat_curly_brackets(answer)}"

        if explanations != None:
            explanations_str = f"explanation: {reformat_curly_brackets(explanations)}"
        
        if marks != None:
            marks_str = f"marks : {reformat_curly_brackets(marks)}"
                    
        if similar_problems != None:
            similar_problems_str = f"similar problems : "
            for i in similar_problems:
                similar_problems_str += reformat_curly_brackets(i)
                similar_problems += ", "

        if improvements != None:
            improvements_str = f"improvements: {reformat_curly_brackets(improvements)}"       

        if hints != None:
            hints_str = f"hints: {hints}"   
            for i in hints:
                hints_str += reformat_curly_brackets(i) 
                hints += ", "   


    wolfram_text = ""
    # if session == None:
    if question == None:
        wolfram_text = reformat_curly_brackets(get_wolframalpha_response(query))
        # st.write(wolfram_text)
        # wolfram_text = convert_to_markdown(wolfram_text)

    # Create the retrieval chain
    template1 = """
    You are a helpful AI math tutor.
    Always give the response in correct markdown format. for the mathematical equations and the signs always use the 100 percent correct mathml format, but never use latex.
    Student has tried a question and all the data related to that question has been provided such as question, answer, explanation, marks, similar problems, improvements, hints and history. These are the data that has been provided to you to generate the answer.\n"""+'Original question: '+question_str+'\n'+"Student provided answer: "+answer_str +'\n'+"Given marks by the system:"+str(marks) +'\n'+"Explanation given by the system: "+explanations_str +'\n'+"Allocated marks for the provided answer: "+marks_str +'\n'+"Improvements can be done to student's answer: "+improvements_str +'\n'+"Previous chat history: "+history  +'\n'+"Similar problems to the problem student has just tried: "+similar_problems_str +'\n'+"Hints generated for the student: "+hints_str+'\n'+"""
    Student may ask the questions about the above data. If the student is asking more questions go beyond the above context and explain and answer with your knowledge. If the student asks beyond the mathematics, you should kindly ask him to ask only math-related questions. You can use the textbook content to generate the answer if it is relevant to the question. If in the provided context, the marks allocated for each step is given, you can show it as the marking scheme. Answer in friendly, explaining manner. Do not give short answers. Always try to explain the answer in detail. If the student asks to generate mathematical steps, always try to go with the steps provided in the explanation. If you can see more relevant information in the textbook content, you can use that information to generate the answer.
    textbook content:""" +relevent_textbook_content+ """
    context: {context}
    input: {input}
    answer:
    """

    template2 = """
    You are a helpful EduGenius AI math tutor.
    Always give the response in correct markdown format. for the mathematical equations and the signs always use the 100 percent correct mathml format, but never use latex.
    try to answer the user query. Always try to follow the steps and the answer provided as the potential answer if it is given. 
    If the potential answer is not relevant to the question or mathematics, igonre it and answer the question with your knowledge.
    If you are asked to generate mathematical steps, always try to go with the steps provided as the potential answer explaining each step more. 
    If you can see more relevant information in the textbook content, you can use that information to generate the answer.
    If the user asks beyond the mathematics, you should kindly ask him to ask only math-related questions.
    Follow the above steps thouroughly and answer in friendly, explaining manner.
    textbook content:""" +relevent_textbook_content+ """
    potential_answer:"""+ wolfram_text+"""
    context: {context}
    input: {input}
    answer:
    """
    template = template2
    if session != None:
        if question != None:
            template = template1

    formatted_user_question = reformat_curly_brackets(query)
    prompt = PromptTemplate.from_template(template)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    response=retrieval_chain.invoke({"input":formatted_user_question})

    return response



def respond_for_user_question(user_question,llm):
    response = QA_RAG(user_question, llm,"vectorstore_text_books","vectorstore_2018_OL", 2, 0.4, dict(st.session_state))
    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
    with st.chat_message("assistant"):
        st.write(response["answer"])



# def respond_for_user_question(user_question,llm):
#     """Generate the platform response for the user queries

#     Args:
#         user_question (string): User's query
#         llm (langchain.models.LLM): LLM model to be used to generate the answer  

#     Returns:
#         string : generated response for the user query
#     """



#     # Textbook Vector Store data rerical
#     vector_textbook = Chroma(persist_directory='vectorstore_text_books', embedding_function=embeddings)
#     textbook_retriver = vector_textbook.as_retriever(
#         search_type="similarity_score_threshold",
#         search_kwargs={'score_threshold': 0.4}
#     )
#     relevent_textbook_documents = textbook_retriver.get_relevant_documents(user_question)
#     relevent_textbook_content = get_page_content(relevent_textbook_documents)
    
#     # Questions vectorstore data retival chain
#     vectordb = Chroma(persist_directory='vectorstore_2018_OL', embedding_function=embeddings)
#     retriever = vectordb.as_retriever(search_kwargs={"k": 2})

#     # Get session data
    
#     ## Chat History
#     history = "history: "
#     for message in st.session_state.messages:
#         history += reformat_curly_brackets(message["content"]) + " "

#     question_str = ''
#     answer_str = ''
#     explanations_str = ''
#     marks_str = ''
#     similar_problems_str = ''
#     improvements_str = ''
#     hints_str = ''

#     question = st.session_state["question_text"]
#     answer = st.session_state["answer"]
#     explanations = st.session_state["explanation"]
#     marks = st.session_state["marks"]
#     similar_problems = st.session_state["similar_problems"]
#     improvements = st.session_state["improvement"]
#     hints = st.session_state["hints"]
    
#     if question != None:
#         question_str = f"question : {reformat_curly_brackets(question)}"

#     if answer != None:
#         answer_str = f"provided answer : {reformat_curly_brackets(answer)}"

#     if explanations != None:
#         explanations_str = f"explanation: {reformat_curly_brackets(explanations)}"
    
#     if marks != None:
#         marks_str = f"marks : {reformat_curly_brackets(marks)}"
                
#     if similar_problems != None:
#         similar_problems_str = f"similar problems : "
#         for i in similar_problems:
#             similar_problems_str += reformat_curly_brackets(i)
#             similar_problems += ", "

#     if improvements != None:
#         improvements_str = f"improvements: {reformat_curly_brackets(improvements)}"       

#     if hints != None:
#         hints_str = f"hints: {hints}"   
#         for i in hints:
#             hints_str += reformat_curly_brackets(i) 
#             hints += ", "   


#     wolfram_text = ""
#     # if question == None:
#     #     wolfram_text = get_wolframalpha_response(user_question)
#     #     # print(wolfram_text)
#     #     wolfram_text = convert_to_markdown(wolfram_text)


#     # Create the retrieval chain
#     template1 = """
#     You are a helpful AI math tutor.
#     Answer based on the following data provided.
#     \n"""+ question_str +'\n'+ answer_str +'\n'+ explanations_str +'\n'+ marks_str +'\n'+ improvements_str +'\n'+ history  +'\n'+ similar_problems_str +'\n'+ hints_str+'\n'+"""
    
#     textbook content:""" +relevent_textbook_content+ """
    
#     context: {context}
#     input: {input}
#     answer:
#     """

#     template2 = """
#     You are a helpful AI math tutor.
#     try to answer the user query. Try to follow the steps provided in the context.Ignore the context.
#     Answer in friendly, explaining manner.
#     textbook content:""" +relevent_textbook_content+ """
#     potential_answer:"""+ wolfram_text+"""
#     context: {context}


#     input: {input}
#     answer:
#     """
#     template = template2
#     if question != None:
#         template = template1

#     formatted_user_question = reformat_curly_brackets(user_question)
#     prompt = PromptTemplate.from_template(template)
#     combine_docs_chain = create_stuff_documents_chain(llm, prompt)
#     retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
#     response=retrieval_chain.invoke({"input":formatted_user_question})
#     # print("Question -----------------------------------------")
#     # print(formatted_user_question)
#     # print("Answer -------------------------------------------")
#     # print(response["answer"])
#     # print("Context ------------------------------------------")
#     # print(response["context"])
#     # print("template -----------------------------------------")
#     # print(template)


#     with st.chat_message("assistant"):
#         st.write(response["answer"])

#     return response
