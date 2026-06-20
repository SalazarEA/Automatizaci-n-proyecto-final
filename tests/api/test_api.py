import pytest
import requests


def validate_common_response(response: requests.Response, expected_status: int) -> dict:
    assert response.status_code == expected_status
    assert response.headers["Content-Type"].startswith("application/json")
    if response.text:
        return response.json()
    return {}


@pytest.mark.api
def test_list_users_returns_page_and_data(user_api):
    response = user_api.list_users(page=2)
    data = validate_common_response(response, 200)

    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert data["page"] == 2
    assert data["total_pages"] >= 1
    assert all("id" in user for user in data["data"])


@pytest.mark.api
def test_get_user_not_found_returns_404(user_api):
    response = user_api.get_user(9999)

    assert response.status_code == 404
    assert response.headers["Content-Type"].startswith("application/json")
    assert response.text == "{}"


@pytest.mark.api
def test_create_update_patch_get_delete_user_flow(user_api):
    create_response = user_api.create_user("morpheus", "leader")
    create_data = validate_common_response(create_response, 201)

    assert create_data["name"] == "morpheus"
    assert create_data["job"] == "leader"
    assert create_data["id"]
    assert "createdAt" in create_data

    user_id = create_data["id"]

    patch_response = user_api.patch_user(user_id, {"job": "Lead QA"})
    patch_data = validate_common_response(patch_response, 200)
    assert patch_data["job"] == "Lead QA"
    assert "updatedAt" in patch_data

    get_response = user_api.get_user(user_id)
    assert get_response.status_code in (200, 404)

    delete_response = user_api.delete_user(user_id)
    assert delete_response.status_code == 204


@pytest.mark.api
def test_login_invalid_credentials_returns_error(user_api):
    response = user_api.login("invalid@example.com", "badpassword")
    assert response.status_code == 400
    payload = response.json()
    assert payload.get("error") == "user not found"
