from pyinstrument import Profiler
import bcrypt

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from auth.hasher import Hasher



FILE = "hasher_performance_profiling.txt"
hr = '_____________________________________________________________________________________________________________________________________________'

profiler =  Profiler()

with open(FILE, 'w') as file:
    pass 
file = open(FILE, "a") 


# mock password list for testing.
passwords = ['12345', 'abcdef', '%##@zxcvbn9087']

# pick one password for testing from the above list
password = '%##@zxcvbn9087'


def test_performance_profile_hasher():
    profiler.start()
    val = Hasher(passwords=passwords)
    profiler.stop()

    file.write(hr)
    file.write(f"\nPerformance Profiling for Hasher()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()


def test_performance_profile_hasher_generate():
    hasher = Hasher(passwords=password)

    profiler.start()
    hashed_pws = hasher.generate()
    profiler.stop()

    file.write(hr)
    file.write(f"\nPerformance Profiling for Hasher()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()

    


test_performance_profile_hasher()
test_performance_profile_hasher_generate()