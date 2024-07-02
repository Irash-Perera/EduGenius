from langchain_google_genai import GoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from create_db import embeddings
from env import API_KEY
import os
import time

os.environ['GOOGLE_API_KEY'] = API_KEY
llm = GoogleGenerativeAI(model = "gemini-pro", temperature=0.7)

def generate_ans(question, llm, embeddings, persist_directory):
    # load the vector store
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    time.sleep(2)
    
    template = """You are a helpful AI tutor. Answer the math problem as mentioned in the context. Explain the answer from the context as much as possible with your mathematical knowledge. Always give correct and clear answers. Sometimes there may be a description in the context explaining diagram too. explain it too as much as possible.Dont give just the answer. Give the explanation too.
    context:{context}
    input: {input}
    answer:
    """
    
    retriever = vectorstore.as_retriever()
    prompt = PromptTemplate.from_template(template)
    combined_doc_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combined_doc_chain)
    
    result = retrieval_chain.invoke({"input": question})
    print(result)
    return result['answer']

answer = generate_ans("**15. Find the income tax that a person who earns an annual income of 800 000 rupees has to pay according to this table.**", llm, embeddings, 'vectorstore_2018_OL')
print("Answer:\n")
print(answer)