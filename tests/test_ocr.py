import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ocr.ocr import *

"""
To run this test script go to EduGenius folder in terminal and enter the following command
pytest .\tests\test_ocr.py
"""

def test_ninja_ocr():
    """
    Functionality: Unit testing of ninja OCR api call
    """
    assert type(ninja_OCR("ocr/testing/test_data/test01.png"))==str

def test_Gemini_Flash_OCR():
    """
    Functionality: Unit testing of Gemini Flash OCR api call
    """
    assert type(Gemini_Flash_OCR("ocr/testing/test_data/test01.png"))==str

def test_Gemini_Pro_OCR():
    """
    Functionality: Unit testing of Gemini Pro OCR api call
    """
    assert type(Gemini_Pro_OCR("ocr/testing/test_data/test01.png"))==str

