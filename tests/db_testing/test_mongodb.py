import pytest
from pymongo import MongoClient
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from auth.hasher import Hasher

# Define the MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://edugenius:edugenius123@edugenius.rnm1rka.mongodb.net/?appName=edugenius")


@pytest.fixture(scope="module")
def mongo_client():
    """

    Yields:
        mongo_client (MongoDB Client): Mongodb clent to access the database.
    """
    client = MongoClient(MONGO_URI)
    db = client['test_db']  
    collection = db['user']
    
    collection.delete_many({})
    
    yield collection
    
    collection.delete_many({})
    client.close()


def test_create_user(mongo_client):
    """Check whether the user instance can be created.

    Args:
        mongo_client (MongoDB Client): Mongodb clent to access the database.
    """
    password = "create_password"
    email = "createuser@example.com"
    name = "Create User"
    
    hashed_password = Hasher([password]).generate()[0]
    mongo_client.insert_one({'password': hashed_password, 'email': email, 'name': name})
    
    inserted_user = mongo_client.find_one({'email': email})
    assert inserted_user is not None
    assert inserted_user['password'] == hashed_password
    assert inserted_user['email'] == email
    assert inserted_user['name'] == name

def test_read_user(mongo_client):
    """Check whether the a user instance can be read.

    Args:
        mongo_client (MongoDB Client): Mongodb clent to access the database.
    """
    
    email = "createuser@example.com"
    user = mongo_client.find_one({'email': email})
    
    assert user is not None
    assert user['email'] == email


def test_update_user(mongo_client):
    """Check whether the user is uppdated after updating the database.

    Args:
        mongo_client (MongoDB Client): Mongodb clent to access the database.
    """
    # Arrange
    email = "createuser@example.com"
    new_name = "Updated Create User"
    
    # Act
    result = mongo_client.update_one({'email': email}, {'$set': {'name': new_name}})
    
    # Assert
    updated_user = mongo_client.find_one({'email': email})
    assert result.modified_count == 1
    assert updated_user is not None
    assert updated_user['name'] == new_name


def test_delete_user(mongo_client):
    """Check whether the user is deleted from the database after deleting a instance.

    Args:
        mongo_client (MongoDB Client): Mongodb clent to access the database.
    """
    email = "createuser@example.com"
    
    result = mongo_client.delete_one({'email': email})
    
    assert result.deleted_count == 1
    deleted_user = mongo_client.find_one({'email': email})
    assert deleted_user is None


# def test_no_duplicate_emails(mongo_client):
#     """Check if the database throws an exception when trying to insert a user with a duplicate email

#     Args:
#         mongo_client (_type_): _description_
#     """
#     # Arrange
#     password = "duplicate_password"
#     email = "duplicateuser@example.com"
#     name = "Duplicate User"
    
#     # Act
#     hashed_password = Hasher([password]).generate()[0]
#     mongo_client.insert_one({'password': hashed_password, 'email': email, 'name': name})
    
#     # Try to insert the same email again
#     with pytest.raises(Exception):  # Assuming duplicate email throws an exception
#         mongo_client.insert_one({'password': hashed_password, 'email': email, 'name': name})


def test_password_hashing(mongo_client):
    """Test whether the password is hashed after storing in the database

    Args:
        mongo_client (MongoDB Client): Mongodb clent to access the database.
    """
    password = "password_to_hash"
    email = "hashcheck@example.com"
    name = "Hash Check"
    
    hashed_password = Hasher([password]).generate()[0]
    mongo_client.insert_one({'password': hashed_password, 'email': email, 'name': name})
    inserted_user = mongo_client.find_one({'email': email})
    
    assert inserted_user['password'] != password
    assert inserted_user['password'] == hashed_password
