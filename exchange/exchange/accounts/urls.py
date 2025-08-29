from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, profile, delete_account, CustomPasswordChangeView

app_name = "accounts"

urlpatterns = [
    path("signin/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="signin"),
    path("join/", SignUpView.as_view(), name="join"),
    path("signout/", auth_views.LogoutView.as_view(next_page="shop:all_products"), name="signout"),
    path("dashboard/", profile, name="dashboard"),
    path("account/remove/", delete_account, name="account_remove"),
    path("password/update/",CustomPasswordChangeView.as_view(template_name="registration/password_update.html"),name="password_update",),
    path("password/updated/",auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_updated.html"),name="password_updated"),
]
