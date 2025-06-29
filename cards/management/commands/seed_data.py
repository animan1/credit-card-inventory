from datetime import date

from django.core.management.base import BaseCommand

from cards.models import Benefit, Card, CardBenefit, Issuer, SpendingCategory


def seed_issuers():
    for name in ["Chase", "Amex"]:
        issuer, created = Issuer.objects.get_or_create(name=name)
        if created:
            print(f"🆕 Created issuer: {name}")
        else:
            print(f"✅ Issuer exists: {name}")


def seed_cards():
    issuers = {issuer.name: issuer for issuer in Issuer.objects.all()}

    cards = [
        {
            "name": "Chase Sapphire Reserve",
            "issuer": issuers.get("Chase"),
            "annual_fee": 795.00,  # updated fee
            "open_date": date(2016, 8, 21),
            "close_date": None,
        },
        {
            "name": "Amex Platinum",
            "issuer": issuers.get("Amex"),
            "annual_fee": 695.00,
            "open_date": date(2020, 6, 1),
            "close_date": None,
        },
        {
            "name": "Amex Gold",
            "issuer": issuers.get("Amex"),
            "annual_fee": 250.00,
            "open_date": date(2021, 3, 15),
            "close_date": None,
        },
    ]

    for card_data in cards:
        card, created = Card.objects.get_or_create(
            name=card_data["name"],
            issuer=card_data["issuer"],
            defaults={
                "annual_fee": card_data["annual_fee"],
                "open_date": card_data["open_date"],
                "close_date": card_data["close_date"],
            },
        )
        if created:
            print(f"🆕 Created card: {card.name}")
        else:
            print(f"✅ Card exists: {card.name}")


def seed_benefits():
    benefits = [
        {
            "name": "Statement Credit",
            "category": Benefit.Category.STATEMENT_CREDIT,
            "description": "A fixed credit amount reimbursed for eligible purchases",
        },
        {
            "name": "Lounge Access",
            "category": Benefit.Category.LOUNGE_ACCESS,
            "description": "Access to airport lounges such as Priority Pass, Centurion, or airline-specific lounges",
        },
        {
            "name": "Points Multiplier",
            "category": Benefit.Category.POINTS_MULTIPLIER,
            "description": "Earn additional points on specific spend categories",
        },
        {
            "name": "Complimentary Membership",
            "category": Benefit.Category.MEMBERSHIP,
            "description": "Subscription or membership included with card",
        },
        {
            "name": "Extended Warranty",
            "category": Benefit.Category.OTHER,
            "description": "Extended protection on purchases beyond manufacturer warranty",
        },
    ]

    for benefit_data in benefits:
        benefit, created = Benefit.objects.get_or_create(
            name=benefit_data["name"],
            defaults={
                "category": benefit_data["category"],
                "description": benefit_data["description"],
            },
        )
        if created:
            print(f"🆕 Created benefit: {benefit.name}")
        else:
            print(f"✅ Benefit exists: {benefit.name}")


def seed_card_benefits():
    csr = Card.objects.get(name="Chase Sapphire Reserve")
    benefits = {
        "Lounge Access": "Priority Pass",
        "Statement Credit": "Annual Travel Credit",
        "Points Multiplier": "3x Points on Travel",
    }

    for benefit_name, display_name in benefits.items():
        benefit = Benefit.objects.get(name=benefit_name)
        cb, created = CardBenefit.objects.get_or_create(
            card=csr,
            display_name=display_name,
            defaults={"benefit": benefit},
        )
        if created:
            print(f"🆕 Linked {display_name} to {csr.name}")
        else:
            print(f"✅ Benefit already linked: {display_name}")


def seed_spending_categories():
    categories = {
        "Travel": ["Airfare", "Hotels", "Train", "Rideshare", "Cruise"],
        "Dining": ["Restaurants", "Bars", "Delivery"],
        "Groceries": [],
        "Gas": [],
        "Entertainment": ["Streaming", "Theater", "Amusement Parks"],
        "Retail": ["Clothing", "Electronics", "General"],
    }

    for parent_name, children in categories.items():
        parent, _ = SpendingCategory.objects.get_or_create(name=parent_name)
        for child_name in children:
            SpendingCategory.objects.get_or_create(name=child_name, parent=parent)


class Command(BaseCommand):
    help = "Seed initial data for Issuers and Cards"

    def handle(self, *args, **options):
        self.stdout.write("Seeding issuers...")
        seed_issuers()
        self.stdout.write("Seeding cards...")
        seed_cards()
        self.stdout.write("Seeding benefits...")
        seed_benefits()
        self.stdout.write("Seeding card benefits...")
        seed_card_benefits()
        self.stdout.write("Seeding spend categories...")
        seed_spending_categories()
        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
