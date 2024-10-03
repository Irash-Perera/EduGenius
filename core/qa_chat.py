
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
import os
from langchain.vectorstores import Chroma
from langchain.chains import VectorDBQA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from utils.createVDB.create_db import embeddings


load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def respond_for_user_question(user_question,llm):
    vectordb = Chroma(persist_directory='vectorstore_2018_OL', embedding_function=embeddings)

    retriever = vectordb.as_retriever(search_kwargs={"k": 5})

    #Create the retrieval chain
    template = """
    You are a helpful AI math tutor.
    Answer based on the following data provided. 
    context: {context}
    input: {input}
    answer:
    """
    prompt = PromptTemplate.from_template(template)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    response=retrieval_chain.invoke({"input":user_question})
    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

    with st.chat_message("assistant"):
        st.write(response["answer"])