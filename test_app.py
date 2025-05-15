# tests/test_app.py

import pytest
from app import app, db, User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def get_token(client):
    response = client.post('/login', json={'username': 'test', 'password': 'pw'})
    return response.get_json()['access_token']

def test_create_and_get_user(client):
    token = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    # Create a new user
    rv = client.post('/users/', json={'username': 'alice', 'email': 'alice@example.com'}, headers=headers)
    assert rv.status_code == 201
    user = rv.get_json()
    assert user['username'] == 'alice'
    assert user['email'] == 'alice@example.com'

    # List users
    rv = client.get('/users/', headers=headers)
    assert rv.status_code == 200
    users = rv.get_json()
    assert len(users) == 1
    assert users[0]['username'] == 'alice'

def test_delete_user(client):
    token = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    # Create and then delete a user
    rv = client.post('/users/', json={'username': 'bob', 'email': 'bob@example.com'}, headers=headers)
    user_id = rv.get_json()['id']
    rv = client.delete(f'/users/{user_id}', headers=headers)
    assert rv.status_code == 204

    # Ensure user is gone
    rv = client.get('/users/', headers=headers)
    assert rv.status_code == 200
    assert rv.get_json() == []
