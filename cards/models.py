from django.db import models
from django.utils.timezone import now


class Issuer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=100)
    issuer = models.ForeignKey("Issuer", on_delete=models.CASCADE, related_name="cards")
    annual_fee = models.DecimalField(max_digits=8, decimal_places=2)
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    benefits = models.ManyToManyField(
        "Benefit", through="CardBenefit", related_name="cards"
    )

    @property
    def is_active(self):
        today = now().date()
        if self.open_date and (not self.close_date or self.close_date > today):
            return True
        return False

    def __str__(self):
        return f"{self.name} ({self.issuer.name})"


class Benefit(models.Model):
    class Category(models.TextChoices):
        LOUNGE_ACCESS = "lounge_access", "Lounge Access"
        POINTS_MULTIPLIER = "points_multiplier", "Points Multiplier"
        STATEMENT_CREDIT = "statement_credit", "Statement Credit"
        MEMBERSHIP = "membership", "Complimentary Membership"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=Category.choices)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CardBenefit(models.Model):
    card = models.ForeignKey(
        "Card", on_delete=models.CASCADE, related_name="card_benefits"
    )
    benefit = models.ForeignKey(
        "Benefit", on_delete=models.CASCADE, related_name="card_benefits"
    )
    display_name = models.CharField(
        max_length=100
    )  # e.g., "Priority Pass", "Travel Credit"
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("card", "display_name")

    def __str__(self):
        return f"{self.card.name}: {self.display_name}"


class SpendingCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )

    class Meta:
        verbose_name = "Spending Category"
        verbose_name_plural = "Spending Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def is_leaf(self):
        return not self.children.exists()

    def get_ancestors(self):
        node = self
        while node.parent:
            yield node.parent
            node = node.parent

    def get_descendants(self):
        for child in self.children.all():
            yield child
            yield from child.get_descendants()
