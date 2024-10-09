import google.generativeai as genai
from langchain.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
import os
from langchain.vectorstores import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from utils.createVDB.create_db import embeddings

from pages.math_solver import get_wolframalpha_response

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def reformat_curly_brackets(text):
    if "{" in text or "}" in text:
        text = text.replace("{", "{{")
        text = text.replace("}", "}}")
    return text


def respond_for_user_question(user_question,llm):
    vectordb = Chroma(persist_directory='vectorstore_2018_OL', embedding_function=embeddings)

    retriever = vectordb.as_retriever(search_kwargs={"k": 2})

    # Get session data
    
    ## Chat History
    history = "history: "
    for message in st.session_state.messages:
        history += reformat_curly_brackets(message["content"]) + " "

    question_str = ''
    answer_str = ''
    explanations_str = ''
    marks_str = ''
    similar_problems_str = ''
    improvements_str = ''
    hints_str = ''

    question = st.session_state["question_text"]
    answer = st.session_state["answer"]
    explanations = st.session_state["explanation"]
    marks = st.session_state["marks"]
    similar_problems = st.session_state["similar_problems"]
    improvements = st.session_state["improvement"]
    hints = st.session_state["hints"]
    
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



    # Create the retrieval chain
    template1 = """
    You are a helpful AI math tutor.
    Answer based on the following data provided.
    \n"""+ question_str +'\n'+ answer_str +'\n'+ explanations_str +'\n'+ marks_str +'\n'+ improvements_str +'\n'+ history  +'\n'+ similar_problems_str +'\n'+ hints_str+'\n'+"""
    context: {context}
    input: {input}
    answer:
    """

    template2 = """
    You are a helpful AI math tutor.
    try to answer the user query. Try to follow the steps provided in the context.Ignore the context.
    Answer in friendly, explaining manner.
    context: {context}


    input: {input}
    answer:
    """
    template = template2
    if question != None:
        template = template1

    formatted_user_question = reformat_curly_brackets(user_question)
    prompt = PromptTemplate.from_template(template)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    response=retrieval_chain.invoke({"input":formatted_user_question})
    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
    # print("Question -----------------------------------------")
    # print(formatted_user_question)
    # print("Answer -------------------------------------------")
    # print(response["answer"])
    # print("Context ------------------------------------------")
    # print(response["context"])
    # print("template -----------------------------------------")
    # print(template)


    with st.chat_message("assistant"):
        st.write(response["answer"])