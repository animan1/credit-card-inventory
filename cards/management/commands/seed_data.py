from cards.models import Issuer
from django.core.management.base import BaseCommand

def seed_issuers():
    for name in ["Chase", "Amex"]:
        issuer, created = Issuer.objects.get_or_create(name=name)
        if created:
            print(f"🆕 Created issuer: {name}")
        else:
            print(f"✅ Issuer exists: {name}")

class Command(BaseCommand):
    help = "Seed initial data for Issuers and Cards"

    def handle(self, *args, **options):
        self.stdout.write("Seeding issuers...")
        seed_issuers()
        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
