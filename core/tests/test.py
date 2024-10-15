from langchain_google_genai import GoogleGenerativeAI
from metrics import RAG_Tester, RAG_Report
import pandas as pd
import time
from dotenv import load_dotenv

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qa_chat import respond_for_user_question, QA_RAG

load_dotenv()
GEMINI_PRO_API_KEY = os.getenv("GEMINI_PRO_API_KEY")
os.environ['GOOGLE_API_KEY'] = GEMINI_PRO_API_KEY
llm = GoogleGenerativeAI(model = "gemini-pro", temperature=0.7)


file_path = os.path.join(os.path.dirname(__file__),'test_data', 'TestCases.xlsx')
df = pd.read_excel(file_path, index_col=False)

vectorstore_marking_scheme_pth = os.path.join(os.path.dirname(__file__),'..','..','vectorstore_2018_OL')
vectorstore_text_books_pth = os.path.join(os.path.dirname(__file__),'..','..','vectorstore_text_books')
# print(vectorstore_marking_scheme_pth)
# print(vectorstore_text_books_pth)
# print()

# test_questions = df["Question"].to_list()
# test_ground_truth =  df["Ground_Truth"].to_list()
# test_answer = []
# test_contexts = []



# for i in range(len(df["Context"].to_list())):
#     test_contexts.append([df["Context"].to_list()[i]])

# rag_tester = RAG_Tester(test_questions, test_answer, test_contexts, test_ground_truth)
# # rag_report = RAG_Report(test_questions, test_answer, test_contexts, test_ground_truth)

# print(rag_tester.faithfulness())
# print(rag_tester.answerRelavance())
# print(rag_tester.contextPrecision())
# print(rag_tester.contextRecall())
# print(rag_tester.contextEntitiesRecall())
# print(rag_tester.contextUtilization())
# print(rag_tester.noiseSensitivity())
# print(rag_tester.aspectCritique("correctness", "Is the submission factually correct?"))

# print(rag_report.generate_report())


def get_context(relevent_documents):
    if relevent_documents == None:
        return None
    else:
        context = []
        for i in relevent_documents:
            context.append(str(i))
        return context



def predict(df):
    test_questions = df["Question"].to_list()
    # test_ground_truth =  df["Ground_Truth"].to_list()
    test_answer = []
    test_contexts = []
        
    for i in range(len(test_questions)):
        print("Processing Question: ", i,'...\n')
        response, wolfram_content, textbook_content,_ = QA_RAG(test_questions[i], llm,vectorstore_text_books_pth,vectorstore_marking_scheme_pth,  2, 0.4)
        test_answer.append(response["answer"])
        print("Context:"+str(response["context"])+'\n\nWolfram content: '+str(wolfram_content)+'\n\nTextbook content: '+str(textbook_content))
        current_context =[]
        current_context.append(str(response["context"]))
        current_context.append(str(wolfram_content))
        current_context.append(str(textbook_content))
        test_contexts.append(current_context)
        print("=========================================================================================\n\n")
    return test_answer,test_contexts
    

def test(df):
    test_questions = df["Question"].to_list()
    test_ground_truth =  df["Ground_Truth"].to_list()
    test_answer, test_contexts = predict(df) 
    # print(test_answer,test_contexts)

    rag_tester = RAG_Tester(test_questions, test_answer, test_contexts, test_ground_truth)


    faithfulness = rag_tester.faithfulness()
    answerRelavance = rag_tester.answerRelavance()
    contextPrecision = rag_tester.contextPrecision()
    contextRecall = rag_tester.contextRecall()
    contextEntitiesRecall = rag_tester.contextEntitiesRecall()
    contextUtilization = rag_tester.contextUtilization()
    noiseSensitivity = rag_tester.noiseSensitivity()
    aspectCritique = rag_tester.aspectCritique("correctness", "Is the submission factually correct?")


    print(faithfulness)
    print(answerRelavance)
    print(contextPrecision)
    print(contextRecall)
    print(contextEntitiesRecall)
    print(contextUtilization)
    print(noiseSensitivity)
    print(aspectCritique)


test(df)

