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

###########################################################################################
"""
Testing the validate_username method of Validator object.
"""
# mock testing values for validate user name.
valid_name = "Makers-of_EduGenius2"
name_with_digits = "123456789"
name_with_small_letters = "checkmancheck"
name_with_capital_letters = "CHECKMANCHECK"
name_with_spaces = "Check Man"
name_with_more_than_20 = 'CheckManCheckManCheckManCheck'


def test_validate_username_with_valid_name(validator):
    """
    Functionality: verify whether user names with expected pattern is well- recognized.
    """
    assert validator.validate_username(valid_name)==True

def test_validate_username_with_digits(validator):
    """
    Functionality: verify whether user names made of only digits is accepted
    """
    assert validator.validate_username(name_with_digits)==True

def test_validate_username_with_smalls(validator):
    """
    Functionality: verify whether user names made of small english letters is accepted.
    """
    assert validator.validate_username(name_with_small_letters)==True

def test_validate_username_with_caps(validator):
    """
    Functionality: verify whether user names made of capital english letters is accepted.
    """
    assert validator.validate_username(name_with_capital_letters)==True

def test_validate_username_with_spaces(validator):
    """
    Functionality: verify whether user names with space is rejected.
    """
    assert validator.validate_username(name_with_spaces)==False

def test_validate_username_lengthy(validator):
    """
    Functionality: verify whether user with more than 20 characters is rejected.
    """
    assert validator.validate_username(name_with_more_than_20)==False

###########################################################################################
"""
Testing the validate_email method of Validator object.
"""    

# mock email test values
invalid_length_2 = "@."
invalid_length_320 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
invalid_mail_without_at = 'zxcdomain.com'
valid_email = 'zxc@domain.com'


def test_validate_email_length_2(validator):
    assert len(invalid_length_2) == 2

    assert validator.validate_email(invalid_length_2) == False

def test_validate_email_length_320(validator):
    assert len(invalid_length_320) == 320

    assert validator.validate_email(invalid_length_320) == False

def test_validate_email_without_at(validator):
    # verifyig the length constraint
    assert 2 < len(invalid_mail_without_at) < 320

    # verifying @ is not present
    assert not('@' in invalid_mail_without_at)

    # verifying whether the mail_id is rejected
    assert validator.validate_email(invalid_mail_without_at) == False

def test_validate_email_valid_mail(validator):
    # verifyig the length constraint
    assert 2 < len(valid_email) < 320

    # verifying @ is not present
    assert '@' in valid_email

    # verifying whether the mail_id is rejected
    assert validator.validate_email(valid_email) == True
