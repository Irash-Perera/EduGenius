import pytest
from datetime import datetime, timedelta

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth.authenticate import Authenticate
from auth.db import collection


@pytest.fixture
def authenticate():
    return Authenticate(collection, 'cookie_name', 'key', cookie_expiry_days=30.0)

def test_set_exp_date(authenticate):
    """
    Functionality: verifies this functions returns a float value.
                :verifies whetther it returns correct expiry date.
    """
    exp_date = authenticate._set_exp_date()

    # asserting float type return
    assert type(exp_date) == float

    # verifies that the expiry date is set to the correct number of days ahead in the future
    cookie_expiry_days = authenticate.cookie_expiry_days
    expected_exp_date = (datetime.utcnow() + timedelta(days=cookie_expiry_days)).timestamp()
    assert pytest.approx(exp_date, rel=1e-9) == expected_exp_date

    