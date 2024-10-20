import pytest
from unittest.mock import MagicMock, patch, Mock
from pymongo.collection import Collection
import streamlit as st
import jwt

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth.authenticate import Authenticate
from auth.db import collection


@pytest.fixture
def authenticate():
    return Authenticate(collection, 'cookie_name', 'key', cookie_expiry_days=30.0)


def test_token_decode(authenticate):
    """
    Functionality: verifies that a valid token is decoded correctly.
    """
    token = jwt.encode({'name': 'abc', 'email': 'abc@mail.com'}, authenticate.key, algorithm='HS256')
    authenticate.token = token
    assert authenticate._token_decode() == {'name': 'abc', 'email': 'abc@mail.com'}

def test_token_decode_with_invalid_token(authenticate):
    """
    Functionality: verifies that an invalid token returns False.
    """
    authenticate.token = 'invalid_token'
    assert authenticate._token_decode() == False

def test_token_decode_with_expired_token(authenticate):
    """
    Functionality: verifies that an expired token returns False.
    """
    token = jwt.encode({'name': 'abc', 'email': 'abc@mail.com', 'exp': 1643723400}, authenticate.key, algorithm='HS256')
    authenticate.token = token
    assert authenticate._token_decode() == False

@patch('jwt.decode')
def test_token_decode_with_jwt_decode_error(mock_jwt_decode, authenticate):
    """
    Functionality: verifies that token_decode returns false when jwt.decode raises an error.
    """
    authenticate.token = 'token'
    mock_jwt_decode.side_effect = jwt.ExpiredSignatureError
    
    assert authenticate._token_decode() == False