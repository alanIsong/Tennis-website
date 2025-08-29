from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Order, OrderItem


def thanks(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order/confirmation.html", {"order": order})


class OrderHistory(LoginRequiredMixin, View):
    def get(self, request):
        email = request.user.email
        orders = Order.objects.filter(emailAddress=email)
        return render(request, "order/history.html", {"orders": orders})


class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, order_id):
        email = request.user.email
        order = get_object_or_404(Order, id=order_id, emailAddress=email)
        items = OrderItem.objects.filter(order=order)
        return render(request, "order/detail.html", {"order": order, "order_items": items})


class CancelOrder(LoginRequiredMixin, View):
    def post(self, request, order_id):
        email = request.user.email
        order = get_object_or_404(Order, id=order_id, emailAddress=email)
        order.delete()
        return render(request, "order/cancelled.html", {"order_id": order_id})
