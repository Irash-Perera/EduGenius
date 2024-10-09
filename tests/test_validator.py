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


valid_name = "Makers-of_EduGenius2"
name_with_spaces = "Monkey Flies"
name_with_more_than_20 = 'Zimba123ZorenDilemmaTranscent'


def test_validate_username_with_valid_name(validator):
    assert validator.validate_username(valid_name)==True

def test_validate_username_with_spaces(validator):
    assert validator.validate_username(name_with_spaces)==False


    

