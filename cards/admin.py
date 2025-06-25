from django.contrib import admin
from .models import Issuer

@admin.register(Issuer)
class IssuerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
