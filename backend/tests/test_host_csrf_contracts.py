import pytest
from django.test import Client, override_settings


@pytest.mark.integration
@override_settings(ALLOWED_HOSTS=["localhost", "127.0.0.1", "testserver"])
def test_disallowed_host_rejected_by_middleware():
    client = Client()
    response = client.get("/admin/login/", HTTP_HOST="bff:8000")
    assert response.status_code == 400


@pytest.mark.integration
@override_settings(ALLOWED_HOSTS=["localhost", "127.0.0.1", "testserver", "bff"])
def test_allowed_host_can_reach_admin_login():
    client = Client()
    response = client.get("/admin/login/", HTTP_HOST="bff:8000")
    assert response.status_code == 200


@pytest.mark.integration
@override_settings(
    ALLOWED_HOSTS=["localhost", "127.0.0.1", "testserver"],
    CSRF_TRUSTED_ORIGINS=["http://localhost:3000"],
)
def test_untrusted_origin_blocked_for_admin_login_post():
    client = Client(enforce_csrf_checks=True)

    get_response = client.get("/admin/login/", HTTP_HOST="localhost:8000")
    csrf_token = get_response.cookies["csrftoken"].value

    post_response = client.post(
        "/admin/login/",
        {
            "username": "nouser",
            "password": "badpass",
            "csrfmiddlewaretoken": csrf_token,
        },
        HTTP_HOST="localhost:8000",
        HTTP_ORIGIN="http://localhost:3101",
        HTTP_REFERER="http://localhost:8000/admin/login/",
    )

    assert post_response.status_code == 403


@pytest.mark.integration
@override_settings(
    ALLOWED_HOSTS=["localhost", "127.0.0.1", "testserver"],
    CSRF_TRUSTED_ORIGINS=["http://localhost:3000", "http://localhost:3101"],
)
def test_trusted_origin_allows_admin_login_post(db_reset):
    client = Client(enforce_csrf_checks=True)

    get_response = client.get("/admin/login/", HTTP_HOST="localhost:8000")
    csrf_token = get_response.cookies["csrftoken"].value

    post_response = client.post(
        "/admin/login/",
        {
            "username": "nouser",
            "password": "badpass",
            "csrfmiddlewaretoken": csrf_token,
        },
        HTTP_HOST="localhost:8000",
        HTTP_ORIGIN="http://localhost:3101",
        HTTP_REFERER="http://localhost:8000/admin/login/",
    )

    # CSRF/origin checks pass; credentials are invalid so admin view re-renders login form.
    assert post_response.status_code == 200
