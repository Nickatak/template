"""Tests for dev seeding and Django admin email login behavior."""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client

User = get_user_model()


@pytest.mark.integration
class TestAdminSeed:
    def test_seed_dev_creates_admin_capable_user(self, db_reset):
        """seed_dev should create the expected dev user with admin permissions."""
        call_command("seed_dev")

        user = User.objects.get(email="test@ex.com")
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_seed_dev_promotes_existing_user_for_admin_access(self, db_reset):
        """seed_dev should promote an existing dev user for admin access."""
        User.objects.create_user(
            email="test@ex.com",
            password="Qweqwe123",
            is_staff=False,
            is_superuser=False,
        )

        call_command("seed_dev")

        user = User.objects.get(email="test@ex.com")
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_seeded_user_can_log_into_admin_with_email(self, db_reset):
        """The seeded dev user should be able to authenticate and load /admin/."""
        call_command("seed_dev")

        client = Client()
        logged_in = client.login(username="test@ex.com", password="Qweqwe123")
        assert logged_in is True

        response = client.get("/admin/")
        assert response.status_code == 200

    def test_admin_login_page_uses_email_label(self, db_reset):
        """Admin login UI should indicate email as the login identifier."""
        client = Client()
        response = client.get("/admin/login/")

        assert response.status_code == 200
        assert b"Email" in response.content
