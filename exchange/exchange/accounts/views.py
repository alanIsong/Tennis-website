from django.views.generic.edit import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "accounts/join.html"
    success_url = reverse_lazy("shop:all_products")

    def form_valid(self, form):
        response = super().form_valid(form)
        customer_group, _ = Group.objects.get_or_create(name="Customer")
        self.object.groups.add(customer_group)
        login(self.request, self.object)
        return response


@login_required
def profile(request):
    return render(request, "registration/dashboard.html", {"user": request.user})



@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("shop:all_products")
    return redirect("accounts:dashboard")


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_update.html"
    success_url = reverse_lazy("accounts:password_updated")
