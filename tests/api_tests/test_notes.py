import pytest

@pytest.mark.api
def test_create_note(api_client):
    response = api_client.create_note(
        title="Test Note",
        description="This is a test note",
        category="Work"
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()["data"]["title"] == "Test Note", "Title mismatch"