from pyinstrument import Profiler
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from pages.canvas import free_draw, save_drawing 


FILE = "canvas_performance_profiling.txt"
hr = '_____________________________________________________________________________________________________________________________________________'

profiler =  Profiler()

with open(FILE, 'w') as file:
    pass 
file = open(FILE, "a") 


def test_performance_profile_free_draw():
    profiler.start()
    free_draw()
    profiler.stop()

    file.write(hr)
    file.write(f"\nPerformance Profiling for free_draw()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()

    
def test_performance_profile_save_drawing():
    can = free_draw()

    profiler.start()
    save_drawing(can)
    profiler.stop()

    file.write(hr)
    file.write(f"\nPerformance Profiling for free_draw()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()




test_performance_profile_free_draw()
test_performance_profile_save_drawing()