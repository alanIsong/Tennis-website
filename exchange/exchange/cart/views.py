from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse

import stripe
from stripe import StripeError

from shop.models import Product
from .models import Cart, CartItem
from order.models import Order, OrderItem
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm


def _cart_id(request):
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.create()
    return session_key


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))

    try:
        item = CartItem.objects.get(product=product, cart=cart)
        if item.quantity < product.stock:
            item.quantity += 1
            item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(product=product, quantity=1, cart=cart)

    return redirect("cart:view_cart")


def cart_detail(request, total=0, counter=0, cart_items=None):
    discount = Decimal("0.00")
    adjusted_total = Decimal("0.00")
    voucher = None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        total = sum((ci.product.price * ci.quantity for ci in cart_items), start=Decimal("0.00"))
        counter = sum((ci.quantity for ci in cart_items), start=0)
    except ObjectDoesNotExist:
        cart_items = []
        total = Decimal("0.00")
        counter = 0

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = "The Tennis Exchange - Checkout"
    voucher_apply_form = VoucherApplyForm()

    voucher_id = request.session.get("voucher_id")
    try:
        if voucher_id:
            voucher = Voucher.objects.get(id=voucher_id)
            discount = total * (Decimal(voucher.discount) / Decimal("100"))
            adjusted_total = total - discount
            stripe_total = int(adjusted_total * 100)
        else:
            adjusted_total = total
    except Voucher.DoesNotExist:
        adjusted_total = total

    if request.method == "POST":
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "eur",
                        "product_data": {"name": "Order from The Tennis Exchange"},
                        "unit_amount": stripe_total,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                billing_address_collection="required",
                payment_intent_data={"description": description},
                success_url=(
                    request.build_absolute_uri(reverse("cart:checkout"))
                    + f"?session_id={{CHECKOUT_SESSION_ID}}&voucher_id={voucher_id or ''}&cart_total={total}"
                ),
                cancel_url=request.build_absolute_uri(reverse("cart:view_cart")),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return render(
                request,
                "cart/basket.html",
                {
                    "cart_items": cart_items,
                    "total": total,
                    "counter": counter,
                    "error": str(e),
                    "voucher_apply_form": voucher_apply_form,
                    "new_total": adjusted_total,
                    "voucher": voucher,
                    "discount": discount,
                },
            )

    return render(
        request,
        "cart/basket.html",
        {
            "cart_items": cart_items,
            "total": total,
            "counter": counter,
            "voucher_apply_form": voucher_apply_form,
            "new_total": adjusted_total,
            "voucher": voucher,
            "discount": discount,
        },
    )


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        item = CartItem.objects.get(product=product, cart=cart)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect("cart:view_cart")


def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(product=product, cart=cart).delete()
    return redirect("cart:view_cart")


def empty_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        CartItem.objects.filter(cart=cart, active=True).delete()
        cart.delete()
    except Cart.DoesNotExist:
        pass

    if "voucher_id" in request.session:
        del request.session["voucher_id"]

    return redirect("shop:all_products")


def create_order(request):
    try:
        session_id = request.GET.get("session_id")
        if not session_id:
            raise ValueError("Missing session ID.")

        session = stripe.checkout.Session.retrieve(session_id)
        customer = session.customer_details
        if not customer or not customer.address:
            raise ValueError("Incomplete customer details from Stripe.")

        order = Order.objects.create(
            token=session.id,
            total=session.amount_total / 100,
            emailAddress=customer.email,
            billingName=customer.name,
            billingAddress1=customer.address.line1,
            billingCity=customer.address.city,
            billingPostcode=customer.address.postal_code,
            billingCountry=customer.address.country,
            shippingName=customer.name,
            shippingAddress1=customer.address.line1,
            shippingCity=customer.address.city,
            shippingPostcode=customer.address.postal_code,
            shippingCountry=customer.address.country,
        )

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            items = CartItem.objects.filter(cart=cart, active=True)
        except ObjectDoesNotExist:
            return redirect("shop:all_products")

        for ci in items:
            OrderItem.objects.create(
                product=ci.product.name,
                quantity=ci.quantity,
                price=ci.product.price,
                order=order,
            )
            prod = Product.objects.get(id=ci.product.id)
            prod.stock = max(0, prod.stock - ci.quantity)
            prod.save()

        empty_cart(request)
        return redirect("shop:all_products")

    except (ValueError, StripeError, Exception):
        return redirect("shop:all_products")


def thanks(request, order_id):
    order = get_object_or_404(Order, id=order_id, emailAddress=request.user.email)
    return render(request, "order/thanks.html", {"order": order})
