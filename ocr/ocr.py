import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()

GOOGLE_GEN_AI_API_KEY = os.getenv("GOOGLE_GEN_AI_API_KEY")
genai.configure(api_key=GOOGLE_GEN_AI_API_KEY)

NINJA_API_URL = 'https://api.api-ninjas.com/v1/imagetotext'

flash_model = genai.GenerativeModel('gemini-1.5-flash')
pro_model  = genai.GenerativeModel(model_name="gemini-1.5-pro")


def ninja_OCR(file_path):
    image_file_descriptor = open(file_path, 'rb')
    files = {'image': image_file_descriptor}
    r = requests.post(NINJA_API_URL, files=files)
    text = ""
    for i in r.json():
        text += i['text']
        text += " "
    text += "\n"
    return text


def Gemini_Flash_OCR(file_path):
    f = genai.upload_file(path = file_path)
    response = flash_model.generate_content([f, "Your are a helpful AI to extract text from the image. Extract the question from the image and return it in markdown format."])
    return response.text


def Gemini_Pro_OCR(file_path):
    f = genai.upload_file(path = file_path)
    response = pro_model.generate_content([f, "Your are a helpful AI to extract text from the image. Extract the question from the image and return it in markdown format."])
    return response.text


