import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth.utils import generate_random_pw

def test_generate_random_pw():
    """
    Functionality: verifies whether the genearted random password is length of 16.
                : verifies whether the genearted random password is a string.
                : verifies whether the genearted random password is made of alphanumeric characters.
    """
    