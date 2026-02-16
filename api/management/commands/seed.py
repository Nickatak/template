"""
Seed command for dev environment.
Creates a test user for development purposes.
Safe to run multiple times - will skip creating users that already exist.
"""

from django.core.management.base import BaseCommand

from api.models.user import CustomUser


class Command(BaseCommand):
    help = "[DEV] Seed the database with development test data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🌱 Starting dev database seeding..."))
        
        # Seed dev user
        dev_email = "test@ex.com"
        dev_password = "Qweqwe123"
        
        if CustomUser.objects.filter(email=dev_email).exists():
            self.stdout.write(self.style.WARNING(f"  ✓ Dev user '{dev_email}' already exists"))
        else:
            CustomUser.objects.create_user(
                email=dev_email,
                password=dev_password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✓ Dev user created: {dev_email}"
                )
            )
        
        self.stdout.write(self.style.SUCCESS("✅ Dev database seeding complete!"))
