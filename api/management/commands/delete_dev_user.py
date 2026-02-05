"""WARNING: This command is for development purposes only.
DO NOT use in production. This command deletes the hardcoded development user
used for local testing convenience.
"""

from django.core.management.base import BaseCommand

from api.models.user import CustomUser


class Command(BaseCommand):
    help = "[DEV ONLY] Delete the dev user if it exists"

    def handle(self, *args, **options):
        email = "test@ex.com"

        try:
            user = CustomUser.objects.get(email=email)
            user.delete()
            self.stdout.write(
                self.style.SUCCESS(f"Dev user '{email}' deleted successfully")
            )
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"Dev user '{email}' does not exist"))
