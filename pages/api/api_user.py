import requests
from .api_client import ApiClient


class UserApi:

    def __init__(self, client: ApiClient):
        self.client = client

    def list_users(self, page: int = 1) -> requests.Response:
        return self.client.get_users(page=page)

    def get_user(self, user_id: int) -> requests.Response:
        return self.client.get_user(user_id)

    def create_user(self, name: str, job: str) -> requests.Response:
        return self.client.create_user(name, job)

    def update_user(self, user_id: str | int, name: str, job: str) -> requests.Response:
        return self.client.update_user(user_id, name, job)

    def patch_user(self, user_id: str | int, payload: dict) -> requests.Response:
        return self.client.patch_user(user_id, payload)

    def delete_user(self, user_id: str | int) -> requests.Response:
        return self.client.delete_user(user_id)

    def register(self, email: str, password: str) -> requests.Response:
        return self.client.post("/register", json={"email": email, "password": password})

    def login(self, email: str, password: str) -> requests.Response:
        return self.client.post("/login", json={"email": email, "password": password})