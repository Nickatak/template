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

        user, created = CustomUser.objects.get_or_create(
            email=dev_email,
            defaults={
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            user.set_password(dev_password)
            user.save(update_fields=["password"])
            self.stdout.write(self.style.SUCCESS(f"  ✓ Dev admin user created: {dev_email}"))
        else:
            updated_fields = []
            if not user.is_staff:
                user.is_staff = True
                updated_fields.append("is_staff")
            if not user.is_superuser:
                user.is_superuser = True
                updated_fields.append("is_superuser")

            if updated_fields:
                user.save(update_fields=updated_fields)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✓ Dev user '{dev_email}' promoted for admin access"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"  ✓ Dev admin user '{dev_email}' already exists")
                )

        self.stdout.write(self.style.SUCCESS("✅ Dev database seeding complete!"))
