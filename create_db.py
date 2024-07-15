from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from env import GOOGLE_GEN_AI_API_KEY
import time
import os

os.environ['GOOGLE_API_KEY'] = GOOGLE_GEN_AI_API_KEY

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def create_db(text_file, embeddings, persist_directory):
    text_loader = TextLoader(text_file)
    data = text_loader.load()
    
    #TODO text splitting
    r_splitter = RecursiveCharacterTextSplitter(
            separators= [ "$$"],
            chunk_size= 250)
    docs = r_splitter.split_documents(data)
    
    # create embeddings
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory = persist_directory)
    time.sleep(2)
    
    vectordb.persist()
    vectordb = None
    
create_db('2018.txt', embeddings, 'vectorstore_2018_OL' )