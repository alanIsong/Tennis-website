from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name", "price", "category", "stock",
        "available", "created", "updated",
    ]
    list_editable = ["price", "stock", "available"]
    list_filter = ["available", "created", "updated", "category"]
    search_fields = ["name", "description"]
    ordering = ["-created"]
    list_per_page = 25
