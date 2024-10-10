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

