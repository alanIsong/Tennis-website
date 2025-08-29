from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("history/", views.OrderHistory.as_view(), name="history"),
    path("view/<int:order_id>/", views.OrderDetail.as_view(), name="detail"),
    path("confirmation/<int:order_id>/", views.thanks, name="confirmation"),
    path("cancel/<int:order_id>/", views.CancelOrder.as_view(), name="cancel"),
]
