# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# from utils import random_email_generator

# EMAIL = ""
# PASSWORD = "Test1234"

# options = Options()
# service = Service('./chromedriver.exe')
# driver = webdriver.Chrome(service=service, options=options)


# driver.get("https://edugenius.streamlit.app/")
# driver.implicitly_wait(10)

# # print(driver.title)


# def test_load_home():
#     assert driver.title == "Streamlit"


# def test_register():
#     EMAIL = random_email_generator(10)
#     email_input = driver.find_element(By.CSS_SELECTOR,'button[data-testid*="data-testid="stBaseButton-secondaryFormSubmit"]')
#     email_input.send_keys(EMAIL)


from seleniumbase import BaseCase
import time

class ComponentsTest(BaseCase):
    # def test_basic(self):
    #     self.open("https://edugenius.streamlit.app/")
    #     time.sleep(10)
    #     self.save_screenshot("current-screenshot.png")
    
    def test_login(self):
        self.open("https://edugenius.streamlit.app/")
        time.sleep(1000)
        print(self)
        self.type("input[id='text_input_1']", "Hello")

