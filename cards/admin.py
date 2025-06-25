from django.contrib import admin

from .models import Benefit, Card, CardBenefit, Issuer, SpendingCategory


@admin.register(Issuer)
class IssuerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "issuer",
        "annual_fee",
        "open_date",
        "close_date",
        "is_active_display",
    )
    list_filter = ("issuer",)
    search_fields = ("name",)

    def is_active_display(self, obj):
        return obj.is_active

    is_active_display.boolean = True
    is_active_display.short_description = "Active?"


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(CardBenefit)
class CardBenefitAdmin(admin.ModelAdmin):
    list_display = ("card", "display_name", "benefit")
    list_filter = ("benefit__category",)
    search_fields = ("card__name", "benefit__name", "display_name")


@admin.register(SpendingCategory)
class SpendingCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)
    list_filter = ("parent",)
