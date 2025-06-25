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

    @property
    def is_active(self):
        today = now().date()
        if self.open_date and (not self.close_date or self.close_date > today):
            return True
        return False

    def __str__(self):
        return f"{self.name} ({self.issuer.name})"
