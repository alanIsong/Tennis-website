from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        ("Product", {"fields": ["product"]}),
        ("Quantity", {"fields": ["quantity"]}),
        ("Price", {"fields": ["price"]}),
    ]
    readonly_fields = ["product", "quantity", "price"]
    can_delete = False
    extra = 0
    max_num = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "billingName", "emailAddress", "created"]
    list_display_links = ("id", "billingName")
    search_fields = ["id", "billingName", "emailAddress"]
    readonly_fields = [
        "id", "token", "total", "emailAddress", "created",
        "billingName", "billingAddress1", "billingCity",
        "billingPostcode", "billingCountry",
        "shippingName", "shippingAddress1", "shippingCity",
        "shippingPostcode", "shippingCountry",
    ]
    fieldsets = [
        ("Order Details", {"fields": ["id", "token", "total", "created"]}),
        ("Billing Details", {
            "fields": [
                "billingName", "billingAddress1", "billingCity",
                "billingPostcode", "billingCountry", "emailAddress",
            ]
        }),
        ("Shipping Details", {
            "fields": [
                "shippingName", "shippingAddress1", "shippingCity",
                "shippingPostcode", "shippingCountry",
            ]
        }),
    ]
    inlines = [OrderItemInline]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Order, OrderAdmin)
