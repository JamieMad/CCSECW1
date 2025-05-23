from api import app
import pytest

@pytest.fixture
def client():
    """Set up a test client for the app with setup and teardown logic."""
    print("\nSetting up the test client")
    with app.test_client() as client:
        yield client  # This is where the testing happens
    print("Tearing down the test client")

def test_documentation(client):
    """Test the swagger route."""
    response = client.get('/swagger')
    assert response.status_code == 200

def test_non_existent(client):
    """Test a non-existant route."""
    response = client.get('/jabawoky')
    assert response.status_code == 404