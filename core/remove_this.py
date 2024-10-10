
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os


load_dotenv()
os.environ['GOOGLE_API_KEY'] =  os.getenv("GOOGLE_GEN_AI_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


vectordb = Chroma(persist_directory='../vectorstore_text_books', embedding_function=embeddings)
retriever = vectordb.as_retriever(search_kwargs={"k": 2})

a = vectordb.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'score_threshold': 0.4}
)


print(a.get_relevant_documents("What is the area of a circle"))
      # print(vectordb.similarity_search_with_relevance_scores("find x", 4))
# print(vectordb.similarity_search("find x")[1].page_content)


