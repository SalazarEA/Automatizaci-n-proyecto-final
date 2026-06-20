import csv
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def resolve_data_path(file_path: str) -> Path:
    candidate = Path(file_path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def load_users_from_csv(file_path: str) -> list[dict[str, str]]:
    file_path = resolve_data_path(file_path)
    users: list[dict[str, str]] = []
    with file_path.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row.get("username", "").strip()
            password = row.get("password", "").strip()
            if username and password:
                users.append({"username": username, "password": password})
    return users


def load_users_from_json(file_path: str) -> list[dict[str, str]]:
    file_path = resolve_data_path(file_path)
    if not file_path.exists():
        return []
    with file_path.open("r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)
    users: list[dict[str, str]] = []
    for entry in data:
        username = str(entry.get("username", "")).strip()
        password = str(entry.get("password", "")).strip()
        if username and password:
            users.append({"username": username, "password": password})
    return users


def load_json_data(file_path: str) -> list[Any]:
    file_path = Path(file_path)
    with file_path.open("r", encoding="utf-8") as jsonfile:
        return json.load(jsonfile)
