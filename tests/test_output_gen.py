from dotenv import load_dotenv
import google.generativeai as genai
import os
import time

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from output_gen import *

load_dotenv()

GOOGLE_GEN_AI_API_KEY = os.getenv("GOOGLE_GEN_AI_API_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

genai.configure(api_key=GOOGLE_GEN_AI_API_KEY)
flash_model = genai.GenerativeModel('gemini-1.5-flash')
pro_model  = genai.GenerativeModel(model_name="gemini-1.5-pro")

from utils.createVDB.create_db import embeddings


## We are not using this fuction instead use OCR
# def test_image_read_call_with_flash():
#     image = open("../assets/data/2019 OLevel/A1.png", 'rb')
#     text = image_read_call(image, flash_model)
#     assert type(text) == str


def test_db_search():
    res = db_search("What is the price?", flash_model, embeddings, '../vectorstore_2018_OL')
    time.sleep(200)
    assert type(res) == str

