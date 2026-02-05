from django.apps import AppConfig
from django.conf import settings


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        """Check for dev user in production and refuse to start.

        The test user (test@ex.com) is created for development convenience using:
            - `make dev-user` or `python manage.py add_dev_user`

        And should be deleted before production deployment using:
            - `make dev-user-delete` or `python manage.py delete_dev_user`

        This check ensures that the test user is not accidentally left in the
        production database, which would be a critical security risk.
        """
        if not settings.DEBUG:
            from api.models.user import CustomUser

            if CustomUser.objects.filter(email="test@ex.com").exists():
                raise SystemExit(
                    "\n🚨 CRITICAL: Development user (test@ex.com) found in production database!\n"
                    "   This is a major security risk. Please delete this user before deploying.\n"
                    "   Use: python manage.py delete_dev_user\n"
                    "   Server startup blocked.\n"
                )
