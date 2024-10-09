import pytest

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from auth.validator import Validator

# create a mock object of Validator
# to use all across the unit testing of the methods of class Validator
@pytest.fixture
def validator():
    return Validator()




