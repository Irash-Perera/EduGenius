from pyinstrument import Profiler
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from auth.validator import Validator



FILE = "validator_performance_profiling.txt"
hr = '_____________________________________________________________________________________________________________________________________________'

profiler =  Profiler()

with open(FILE, 'w') as file:
    pass 
file = open(FILE, "a") 


validator = Validator()


valid_name = "Makers-of_EduGenius2"
valid_name1 = 'user123'
valid_email = 'zxc@domain.com'


def test_performance_profile_validate_username():
    profiler.start()
    validator.validate_username(valid_name)
    profiler.stop()

    file.write(hr)
    file.write(f"\nPerformance Profiling for Validator.validate_username()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()


def test_performance_profile_validate_email():
    profiler.start()
    validator.validate_email(valid_email)    
    profiler.stop()
    file.write(hr)
    file.write(f"\nPerformance Profiling for Validator.validate_email()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()


def test_performance_profile_validate_name():
    profiler.start()
    validator.validate_name(valid_name1)    
    profiler.stop()
    file.write(hr)
    file.write(f"\nPerformance Profiling for Validator.validate_name()\n")
    file.write(hr)
    file.write(profiler.output_text())
    file.write("\n\n")
    
    profiler.reset()

    

test_performance_profile_validate_username()
test_performance_profile_validate_email()
test_performance_profile_validate_name()