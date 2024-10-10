import pytest
import bcrypt

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth.hasher import Hasher


# mock password list for testing.
passwords = ['12345', 'abcdef', '%##@zxcvbn9087']

# pick one password for testing from the above list
password = '%##@zxcvbn9087'

"""
Create a fixture to mock the Hasher object.
So that Hasher object can be reused across all the test cases.
"""
@pytest.fixture
def hasher():
    return Hasher(passwords=passwords)


def test_initialization(hasher):
    """
    Functionality: verify whether Hasher object initialization is as intended.
    """
    # verify the correct assignment of password list
    assert hasher.passwords  == passwords


def test_hash(hasher):
    """
    Functionality: verifies whether _hash method of Hasher correclty hashes the password (check both type and hashed value)
    """

    hashed_pw = hasher._hash(password=password)

    # verify the hashed pw is a string
    assert type(hashed_pw)==str
    
    # verify whether password is not equal to original password.
    assert hashed_pw != password

    # checkpw compares hashed pw and oringinal password in bytes format.
    # we used .encode() methods to convert string into string.
    assert bcrypt.checkpw(password=password.encode(), hashed_password=hashed_pw.encode())


def test_generate(hasher):
    """
    Functionality: verifies the functionality of generate method of Hasher under hasher.py
    """
    hashed_pws = hasher.generate()

    # verify the type of the original password 
    assert type(passwords) == list

    # verify the length of passwords are equal
    assert len(passwords) == len(hashed_pws)

    
    
    for h_pw, pw in zip(hashed_pws, passwords):
        # verify the type of each hashed password as string.
        assert type(h_pw) == str
    
        # verify hashed password is different from original password.
        assert h_pw != pw

        # compare hashed password and original password 
        # 'to verify whether the hashed original password is the actual hased version of it
        assert bcrypt.checkpw(hashed_password=h_pw.encode(), password=pw.encode())
