import logging
from typing import Optional
import requests


class ApiClient:

    def __init__(self, base_url: str, headers: dict | None = None, logger: Optional[logging.Logger] = None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {"Content-Type": "application/json"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.logger = logger or logging.getLogger(__name__)

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json: dict | None = None,
        timeout: int = 10,
    ) -> requests.Response:
        url = self._url(path)
        self.logger.debug(
            "API request %s %s params=%s json=%s",
            method,
            url,
            params,
            json,
        )
        response = self.session.request(method, url, params=params, json=json, timeout=timeout)
        self.logger.debug(
            "API response %s %s status=%s text=%s",
            method,
            url,
            response.status_code,
            response.text,
        )
        return response

    def get(self, path: str, params: dict | None = None, timeout: int = 10) -> requests.Response:
        return self._request("GET", path, params=params, timeout=timeout)

    def post(self, path: str, json: dict | None = None, timeout: int = 10) -> requests.Response:
        return self._request("POST", path, json=json, timeout=timeout)

    def put(self, path: str, json: dict | None = None, timeout: int = 10) -> requests.Response:
        return self._request("PUT", path, json=json, timeout=timeout)

    def patch(self, path: str, json: dict | None = None, timeout: int = 10) -> requests.Response:
        return self._request("PATCH", path, json=json, timeout=timeout)

    def delete(self, path: str, timeout: int = 10) -> requests.Response:
        return self._request("DELETE", path, timeout=timeout)

    # Convenience methods used by tests
    def get_users(self, page: int = 1) -> requests.Response:
        return self.get("/users", params={"page": page})

    def get_user(self, user_id: int) -> requests.Response:
        return self.get(f"/users/{user_id}")

    def create_user(self, name_or_payload, job: str | None = None) -> requests.Response:
        if isinstance(name_or_payload, dict):
            payload = name_or_payload
        else:
            payload = {"name": name_or_payload, "job": job}
        return self.post("/users", json=payload)

    def update_user(self, user_id: str | int, name_or_payload, job: str | None = None) -> requests.Response:
        if isinstance(name_or_payload, dict):
            payload = name_or_payload
        else:
            payload = {"name": name_or_payload, "job": job}
        return self.put(f"/users/{user_id}", json=payload)

    def patch_user(self, user_id: str | int, payload: dict) -> requests.Response:
        return self.patch(f"/users/{user_id}", json=payload)

    def delete_user(self, user_id: str | int) -> requests.Response:
        return self.delete(f"/users/{user_id}")