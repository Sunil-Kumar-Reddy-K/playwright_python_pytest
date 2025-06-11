import requests

class NotesApi:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def create_note(self, title: str, description: str, category: str):
        payload = {
            "title": title,
            "description": description,
            "category": category
        }
        response = requests.post(f"{self.base_url}/notes", json=payload, headers=self.headers)
        return response