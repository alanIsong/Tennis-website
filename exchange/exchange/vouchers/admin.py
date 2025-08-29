from django.contrib import admin
from .models import Voucher


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ["code", "discount", "valid_from", "valid_to", "active"]
    list_filter = ["active", "valid_from", "valid_to"]
    search_fields = ["code"]
    ordering = ["-valid_from"]
    list_editable = ["discount", "active"]
    date_hierarchy = "valid_from"

