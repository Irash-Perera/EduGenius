from pyinstrument import Profiler
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ocr.ocr import *


FILE = "ocr_performance_profiling.txt"
hr = '_____________________________________________________________________________________________________________________________________________'

profiler =  Profiler()

with open(FILE, 'w') as file:
    pass 
file = open(FILE, "a") 



def test_performance_profile_ninja_ocr():
    profiler.start()
    ninja_OCR("test01.png")
    profiler.stop()

    file.write(hr)
    file.write(f"\nPerformance Profiling for ninja_ocr()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()


def test_performance_profile_Gemini_Flash_OCR():
    profiler.start()
    Gemini_Flash_OCR("test01.png")
    profiler.stop()

    file.write(hr)
    file.write(f"\nPerformance Profiling for Gemini_Flash_OCR()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()


def test_performance_profile_Gemini_Pro_OCR():
    profiler.start()
    Gemini_Pro_OCR("test01.png")
    profiler.stop()

    file.write(hr)
    file.write(f"\nPerformance Profiling for Gemini_Pro_OCR()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()


test_performance_profile_ninja_ocr()
test_performance_profile_Gemini_Flash_OCR()
test_performance_profile_Gemini_Pro_OCR()