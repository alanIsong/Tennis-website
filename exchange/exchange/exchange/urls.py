from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("order/", include("order.urls", namespace="order")),
    path("vouchers/", include("vouchers.urls", namespace="vouchers")),
    path("search/", include("search_app.urls", namespace="search_app")),
    path("", include("shop.urls", namespace="shop")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
