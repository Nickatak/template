"""WARNING: This command is for development purposes only.
DO NOT use in production. This command creates a hardcoded development user
with predictable credentials for local testing convenience.
"""

from django.core.management.base import BaseCommand

from api.models.user import CustomUser


class Command(BaseCommand):
    help = "[DEV ONLY] Create a dev user with easy-to-remember credentials"

    def handle(self, *args, **options):
        email = "test@ex.com"
        password = "Qweqwe123"

        # Check if user already exists
        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Dev user '{email}' already exists"))
            return

        # Create the dev user
        CustomUser.objects.create_user(email=email, password=password)
        self.stdout.write(
            self.style.SUCCESS(
                f"Dev user created successfully\n"
                f"  Email: {email}\n"
                f"  Password: {password}"
            )
        )
