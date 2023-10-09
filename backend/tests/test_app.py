import pytest
from flask import json
import sys
sys.path.append('/home/daydreamer/mail_sakusei_jp')
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data  # Assuming your index.html starts with the typical doctype. Adjust this if not.

def test_api_generate_valid_input(client):
    # Dummy valid input
    data = {
        'recipient': 'John Doe',
        'signature': 'Jane Smith',
        'text': 'Please attend the meeting tomorrow.'
    }

    response = client.post('/api/generate', data=json.dumps(data), content_type='application/json')
    print (response.json)
    assert response.status_code == 200
    assert "result" in response.json

def test_api_generate_invalid_input(client):
    # Missing required fields
    data = {
        'recipient': 'John Doe',
        'text': 'Please attend the meeting tomorrow.'

    }

    response = client.post('/api/generate', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400  # Assuming Flask's default 400 for bad requests

def test_api_generate_no_input(client):
    response = client.post('/api/generate')
    assert response.status_code == 400  # Again, assuming Flask's default 400 for bad requests