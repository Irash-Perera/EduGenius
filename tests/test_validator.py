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
    """
    Functionality: verify the rejection of mail address with length 2.
    """
    # verifying whether mail_id is of length of 2
    assert len(invalid_length_2) == 2

    # verify whether the mail_id with length 2 is successfully rejected.
    assert validator.validate_email(invalid_length_2) == False


def test_validate_email_length_320(validator):
    """
    Functionality: verify the rejection of mail address with length 320.
    """
    # verifying whether the mail_id is of length of 320
    assert len(invalid_length_320) == 320

    # verify whether the mail_id with length 320 is successfully rejected.
    assert validator.validate_email(invalid_length_320) == False


def test_validate_email_without_at(validator):
    """
    Functionality: verify the rejection of mail address without '@' symbol.
    """
    # verifyig the length constraint
    assert 2 < len(invalid_mail_without_at) < 320

    # verifying @ is not present
    assert not('@' in invalid_mail_without_at)

    # verifying whether the mail_id is rejected
    assert validator.validate_email(invalid_mail_without_at) == False


def test_validate_email_valid_mail(validator):
    """
    Functionality: verify the acceptance of mail address with length between 2 and 320 and having '@' symbol in it.
    """
    # verifyig the length constraint
    assert 2 < len(valid_email) < 320

    # verifying @ is present
    assert '@' in valid_email

    # verifying whether the mail_id is acctected
    assert validator.validate_email(valid_email) == True


###########################################################################################
"""
Testing the validate_name method of Validator object.
"""    

# mock testing values for names.
invalid_name_length_1='e'
invalid_name_length_100='eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
invalid_name_with_wrong_type = 1110  # not a string value(integer value)
valid_name = 'user123'

def test_validate_name_length_1(validator):
    """
    Functionality: verify the rejection of name with length 1
    """
    # verifying length of the name is 1
    assert len(invalid_name_length_1)==1

    # verify name is of string type
    assert type(invalid_name_length_1)==str

    # verify whether the name with length 1 is successfully rejected.
    assert validator.validate_name(invalid_name_length_1) == False


def test_validate_name_length_100(validator):
    """
    Functionality: verify the rejection of name with length 100
    """
    # verifying length of the name is 100
    assert len(invalid_name_length_100)==100

    # verify name is of string type
    assert type(invalid_name_length_100)==str

    # verify whether the name with length 100 is successfully rejected.
    assert validator.validate_name(invalid_name_length_100) == False


def test_validate_name_of_wrong_type(validator):
    """
    Functionality: verify the rejection of name of non-string type
    """
    # verify name is not of string type
    assert type(invalid_name_with_wrong_type) != str

    # verify whether the name with wrong type causes type error
    with pytest.raises(TypeError):
        validator.validate_name(invalid_name_with_wrong_type)

def test_validate_name_valid_name(validator):
    """
    Functionality: verify the acceptance of the correct name
    """
    # verifying length of the name is 100
    assert 1 < len(valid_name) < 100

    # verify name is of string type
    assert type(valid_name)==str

    # verify whether the name is successfully accepted.
    assert validator.validate_name(valid_name) == True
    