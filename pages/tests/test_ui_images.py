from seleniumbase import BaseCase
import time
import cv2
import numpy as np

DISSIMILARITY_THRESHOLD = 0.0015

class ComponentsTest(BaseCase):
    def test_home(self):
        self.open("https://edugenius.streamlit.app/")
        time.sleep(20)
        self.save_screenshot("test_images/home.png")
        test_image = cv2.imread("test_images/home.png")
        original_image = cv2.imread("original_images/home.png")
        difference = cv2.subtract(test_image, original_image)    
        assert np.sum(difference)/np.sum(original_image) < DISSIMILARITY_THRESHOLD

    def test_about(self):
        self.open("https://edugenius.streamlit.app/about")
        time.sleep(20)
        self.save_screenshot("test_images/about.png")
        test_image = cv2.imread("test_images/about.png")
        original_image = cv2.imread("original_images/about.png")
        difference = cv2.subtract(test_image, original_image)    
        assert np.sum(difference)/np.sum(original_image) < DISSIMILARITY_THRESHOLD


    def test_dashboard(self):
        self.open("https://edugenius.streamlit.app/dashboard")
        time.sleep(20)
        self.save_screenshot("test_images/dashboard.png")
        test_image = cv2.imread("test_images/dashboard.png")
        original_image = cv2.imread("original_images/dashboard.png")
        difference = cv2.subtract(test_image, original_image)    
        assert np.sum(difference)/np.sum(original_image) < DISSIMILARITY_THRESHOLD

    def test_QA(self):
        self.open("https://edugenius.streamlit.app/chat")
        time.sleep(20)
        self.save_screenshot("test_images/chat.png")
        test_image = cv2.imread("test_images/chat.png")
        original_image = cv2.imread("original_images/chat.png")
        difference = cv2.subtract(test_image, original_image)    
        assert np.sum(difference)/np.sum(original_image) < DISSIMILARITY_THRESHOLD


    def test_math_solver(self):
        self.open("https://edugenius.streamlit.app/math_solver")
        time.sleep(20)
        self.save_screenshot("test_images/math_solver.png")
        test_image = cv2.imread("test_images/math_solver.png")
        original_image = cv2.imread("original_images/math_solver.png")
        difference = cv2.subtract(test_image, original_image)    
        assert np.sum(difference)/np.sum(original_image) < DISSIMILARITY_THRESHOLD


    def test_feedbacks(self):
        self.open("https://edugenius.streamlit.app/feedbacks")
        time.sleep(20)
        self.save_screenshot("test_images/feedbacks.png")
        test_image = cv2.imread("test_images/feedbacks.png")
        original_image = cv2.imread("original_images/feedbacks.png")
        difference = cv2.subtract(test_image, original_image)    
        assert np.sum(difference)/np.sum(original_image) < DISSIMILARITY_THRESHOLD


    def test_documentation(self):
        self.open("https://edugenius.streamlit.app/documentation")
        time.sleep(20)
        self.save_screenshot("test_images/documentation.png")
        test_image = cv2.imread("test_images/documentation.png")
        original_image = cv2.imread("original_images/documentation.png")
        difference = cv2.subtract(test_image, original_image)    
        assert np.sum(difference)/np.sum(original_image) < DISSIMILARITY_THRESHOLD




    