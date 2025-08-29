from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.prod_list, name="all_products"),
    path("categories/", views.category_list, name="categories"),
    path("categories/<uuid:category_id>/", views.category_detail, name="category_items"),  
    path("<uuid:category_id>/<uuid:product_id>/", views.product_detail, name="product_detail"),
    path("<uuid:category_id>/", views.prod_list, name="products_by_category"),
]




