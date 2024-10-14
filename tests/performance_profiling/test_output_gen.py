from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
import os
import time
from pyinstrument import Profiler

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from output_gen import *
sys.path.remove(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.createVDB.create_db import embeddings


load_dotenv()

GOOGLE_GEN_AI_API_KEY = os.getenv("GOOGLE_GEN_AI_API_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

genai.configure(api_key=GOOGLE_GEN_AI_API_KEY)
flash_model = GoogleGenerativeAI(model='gemini-1.5-flash')
pro_model  = GoogleGenerativeAI(model="gemini-1.5-pro")





FILE = "output_gen_performance_profiling.txt"
hr = '_____________________________________________________________________________________________________________________________________________'

profiler =  Profiler()

with open(FILE, 'w') as file:
    pass 
file = open(FILE, "a") 



def test_performance_profile_db_search():
    profiler.start()
    res = db_search("What is the price?", flash_model, embeddings, '../vectorstore_2018_OL')
    profiler.stop()

    file.write(hr)
    file.write(f"\nPerformance Profiling for db_search()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()



test_performance_profile_db_search()
