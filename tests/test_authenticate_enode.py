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

def test_init(authenticate):
    """
    Functionality: verifies the intended initialization of Authenticate Object.
    """
    # verifies the assignment of collection object to authenticate object.
    assert authenticate.collection == collection

    # verifies the assignment of cookie name to authenticate object.
    assert authenticate.cookie_name == 'cookie_name'

    # verifies the assignment of key to authenticate  object.
    assert authenticate.key == 'key'

    # verifies the assignment of cookie_expiry_days to authenticate  object.
    assert authenticate.cookie_expiry_days == 30.0

    # verifies the whether name attribute in session state is None.
    assert st.session_state['name'] == None

    # verifies the whether email attribute in session state is None.
    assert st.session_state['email'] == None

    # verifies the whether logout attribute in session state is None.
    assert st.session_state['logout'] == None

    # verifies the whether trace_id attribute in session state is None.
    assert st.session_state['trace_id'] == None

    # verifies the whether message list is empty in session state.
    assert st.session_state.messages == []

    # verifies the whether answer attribute in session state is None.
    assert st.session_state.answer == None

    # verifies the whether answer_image attribute in session state is None.
    assert st.session_state.answer_image == None

    # verifies the whether hints list in session state is Empty.
    assert st.session_state.hints == []

    # verifies the whether marks attribute in session state is None.
    assert st.session_state.marks == None

    # verifies the whether explanation attribute in session state is None.
    assert st.session_state.explanation == None

    # verifies the whether improvement attribute in session state is None.
    assert st.session_state.improvement == None

    # verifies the whether similar_problems attribute in session state is None.
    assert st.session_state.similar_problems == None

    # verifies the whether question attribute in session state is None.
    assert st.session_state.question == None

    # verifies the whether question_text attribute in session state is None.
    assert st.session_state.question_text == None


def test_token_encode(authenticate):
    """
    Functionality: verifies whether _token_encode function correctly encodes and returns string value as expected.
    """
    # modifying session state values after testing the initializtion
    st.session_state['name'] = 'abc'
    st.session_state['email'] = 'abc@mail.com'

    # setting up a mock expiary date value.
    authenticate.exp_date = 1643723400

    # invoke _token_encode
    token = authenticate._token_encode()

    # verifies it returns somthing not null.
    assert token is not None

    # verifes whether it returns a string value or not.
    assert type(token)==str

def test_token_encode_with_invalid_key(authenticate):
    """
    Functionality: verifies whether token_encode invokes TypeError when key is invalid(set to None)
    """
    # Set the exp date to a valid value
    authenticate.exp_date = 1643723400
    
    # Set the key to None to simulate an invalid key
    authenticate.key = None
    
    # Check that a TypeError is raised when the _token_encode method is called
    with pytest.raises(TypeError):
        # Call the _token_encode method
        authenticate._token_encode()


@patch('jwt.encode')
def test_token_encode_with_jwt_encode_error(mock_jwt_encode, authenticate):
    """
    Functionality: verifies whether token_encode raises jwt.ExpiredSignatureError when jwt.encode raises an error.
    """
    # Set the exp date to a valid value
    authenticate.exp_date = 1643723400
    
    # Mock the jwt.encode function to raise a jwt.ExpiredSignatureError
    mock_jwt_encode.side_effect = jwt.ExpiredSignatureError
    
    # Check that a jwt.ExpiredSignatureError is raised when the _token_encode method is called
    with pytest.raises(jwt.ExpiredSignatureError):
        # Call the _token_encode method
        authenticate._token_encode()


def test_token_encode_with_invalid_session_state(authenticate):
    """
    Functionality: verifies when session state is empty(invalid) token_enode throws KeyError.
    """
    # mock expiary date value.
    authenticate.exp_date = 1643723400

    # making session state empty dictionary.
    st.session_state = {}

    # check for the key error.
    with pytest.raises(KeyError):
        authenticate._token_encode()

