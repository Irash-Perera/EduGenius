import google.generativeai as genai
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langfuse import Langfuse
from langfuse.decorators import observe
from env import LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_HOST, GOOGLE_GEN_AI_API_KEY
import PIL.Image
import os
import time

genai.configure(api_key=GOOGLE_GEN_AI_API_KEY)
flash_model = genai.GenerativeModel('gemini-1.5-flash')
pro_model  = genai.GenerativeModel(model_name="gemini-1.5-pro")

os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
os.environ["LANGFUSE_HOST"] = LANGFUSE_HOST

def output_bypass(model, prompt, question_, student_answer):
    response = model.generate_content([prompt, question_, student_answer])
    return response

def hint_bypass(model, prompt, question_):
    response = model.generate_content([ prompt, question_])
    return response

@observe(as_type="generation", capture_output=True)
def image_read_call(f,model):
    response = model.generate_content([f, "Your are a helpful AI to extract text from the image. Extract the question from the image and return it in markdown format."])
    return response.text
  
@observe(as_type="generation", capture_output=True)
def answer_gen_call(model, prompt, question_, student_answer, output):
    response = output
    return response.text

@observe(as_type="generation", capture_output=True)
def hint_gen_call(model, prompt, question_, output):
    response = output
    return response.text

def read_image(question_image_path, model):
    f = genai.upload_file(path = question_image_path)
    file = genai.get_file(name = f.name)
    response = image_read_call(f, model)
    return response

def db_search(question, llm, embeddings, persist_directory):
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
    return result
@observe(as_type="generation", capture_output=True)
def generate_answer(selected_paper, selected_question, selected_file, context, model):
    question_ = PIL.Image.open(os.path.join('data', selected_paper, selected_question))
    student_answer = PIL.Image.open(selected_file)
    
    prompt = """You are a helpful AI math tutor. Here question image and the answer image which was uploaded by the student are given. Also a context is provided. That context includes the information from the original marking scheme and marks for each step. I want you to analyze these information and provide a json file including 
    correctness of the answer(This can be correct, partially correct, or incorrecr), 
    marks obtained by the student(This can only be 0,1 or 2. Explain how they got these marks, If only one answer is given and if it is wrong then 0 marks. If context contains how the marks should be given strictly go with that. Obtainable maximum marks should be 2 ), 
    explanation of the problem and the correct answer, 
    how the uploaded answer can be improve, here analyse the student's answer and provide a way to improve it. 
    and examples of at least 3 similar problems that can be solved using the same method and solve those problems too. If can add more fetures to the json file.
    No need to strictly follow the context. You can use your own knowledge to analyze the answer when the context is not enough and answer is not available in the context. Also the returning json file should not be in the same format as described it can be dynamically changed according to the problem and answer. Use mathml format for the answer in json file. only return the json file in markdown format. Do not inlcude the asked question again in the json file. Names of the sections should be like titles.In the explanations do them as far as you can. Also every section in json file contains only title and content in mathml as 2 subpods called "title" and "content".  nothing more than that. In the every section always do not add more than "title" and "content". This is the context: \n"""+str(context["context"])

    response = output_bypass(model, prompt, question_, student_answer)
    return response

def generate_hints(selected_paper, selected_question, model):
    prompt = """You are a helpful math tutor. I have provided a question to you. Please provide at least three hints and a example to solve the question, as a json file. Do not reveal the answer. only return the json file in markdown format. Do not inlcude the asked question again in the json file. Names of the sections should be like titles.  Also every section in json file contains only title and content in markdown as 2 subpods called "title" and "content".  nothing more than that. In the every section always do not add more than "title" and "content".JSON object should be  a dictionary structure with items."""
    
    question_ = PIL.Image.open(os.path.join('data', selected_paper, selected_question))
    
    response1 = hint_bypass(model, prompt, question_)
    
    return response1
        
