import logging
import os
import sys
import pytest

# Ensure project root is on sys.path so tests can import application packages
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from pages.api.api_client import ApiClient
from pages.api.api_user import UserApi

BASE_URL = "https://reqres.in/api"
HEADERS = {
    "x-api-key": "reqres_0cc670f2c4104826aff9494450208bd0",
    "Content-Type": "application/json",
}


@pytest.fixture(scope="function")
def api_client(api_logger) -> ApiClient:
    return ApiClient(BASE_URL, headers=HEADERS, logger=api_logger)


@pytest.fixture(scope="function")
def api_logger(request):
    logger = logging.getLogger(f"api_{request.node.name}")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    logs_dir = request.config._logs_dir
    log_filename = f"{request.node.name}_api.log"
    log_path = os.path.join(logs_dir, log_filename)

    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)

    yield logger

    handler.close()
    logger.removeHandler(handler)


@pytest.fixture
def user_api(api_client: ApiClient) -> UserApi:
    return UserApi(api_client)
