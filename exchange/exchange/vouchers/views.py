from django.shortcuts import redirect
from django.utils import timezone
from .models import Voucher
from .forms import VoucherApplyForm


def voucher_apply(request):
    """Apply a voucher code to the current session if valid."""
    now = timezone.now()
    if request.method == "POST":
        form = VoucherApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"].strip()
            try:
                voucher = Voucher.objects.get(
                    code__iexact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True,
                )
                request.session["voucher_id"] = voucher.id
            except Voucher.DoesNotExist:
                request.session["voucher_id"] = None
    return redirect("cart:cart_detail")

