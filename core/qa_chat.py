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



def respond_for_user_question(user_question,llm):
    """Generate the platform response for the user queries

    Args:
        user_question (string): User's query
        llm (langchain.models.LLM): LLM model to be used to generate the answer  

    Returns:
        string : generated response for the user query
    """



    # Textbook Vector Store data rerical
    vector_textbook = Chroma(persist_directory='vectorstore_text_books', embedding_function=embeddings)
    textbook_retriver = vector_textbook.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'score_threshold': 0.4}
    )
    relevent_textbook_documents = textbook_retriver.get_relevant_documents(user_question)
    relevent_textbook_content = get_page_content(relevent_textbook_documents)
    
    # Questions vectorstore data retival chain
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


    wolfram_text = ""
    if question == None:
        wolfram_text = get_wolframalpha_response(user_question)
        # print(wolfram_text)
        wolfram_text = convert_to_markdown(wolfram_text)


    # Create the retrieval chain
    template1 = """
    You are a helpful AI math tutor.
    Answer based on the following data provided.
    \n"""+ question_str +'\n'+ answer_str +'\n'+ explanations_str +'\n'+ marks_str +'\n'+ improvements_str +'\n'+ history  +'\n'+ similar_problems_str +'\n'+ hints_str+'\n'+"""
    
    textbook content:""" +relevent_textbook_content+ """
    
    context: {context}
    input: {input}
    answer:
    """

    template2 = """
    You are a helpful AI math tutor.
    try to answer the user query. Try to follow the steps provided in the context.Ignore the context.
    Answer in friendly, explaining manner.
    textbook content:""" +relevent_textbook_content+ """
    potential_answer:"""+ wolfram_text+"""
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

    return response
