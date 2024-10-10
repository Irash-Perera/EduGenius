import pytest
from unittest.mock import MagicMock, patch, Mock
from pymongo.collection import Collection

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth.authenticate import Authenticate  
@pytest.fixture
def mock_collection():
    return Collection(database='database', name='abc')

@pytest.fixture
def authenticate(mock_collection):
    return Authenticate(mock_collection, 'cookie_name', 'key', cookie_expiry_days=30.0)

def test_init(authenticate):
    assert authenticate.collection == mock_collection
    assert authenticate.cookie_name == 'cookie_name'
    assert authenticate.key == 'key'
    assert authenticate.cookie_expiry_days == 30.0


