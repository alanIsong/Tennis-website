from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    total_items = 0
    if "admin" in request.path:
        return {}
    try:
        active_cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        if active_cart:
            cart_entries = CartItem.objects.filter(cart=active_cart)
            for entry in cart_entries:
                total_items += entry.quantity
    except Cart.DoesNotExist:
        total_items = 0
    return {"item_count": total_items}


