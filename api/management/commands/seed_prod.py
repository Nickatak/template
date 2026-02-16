"""
Seed command for prod/staging environment.
Currently a no-op for production safety.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "[PROD] Seed the database (currently disabled for safety)"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                "⚠️  Production seeding is currently disabled.\n"
                "   To add seeding for production, update seed_prod.py with appropriate logic."
            )
        )
