from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("add/<uuid:product_id>/", views.add_cart, name="add_item"),
    path("", views.cart_detail, name="view_cart"),
    path("remove/<uuid:product_id>/", views.cart_remove, name="remove_item"),
    path("delete/<uuid:product_id>/", views.full_remove, name="delete_item"),
    path("checkout/", views.create_order, name="checkout"),
]
