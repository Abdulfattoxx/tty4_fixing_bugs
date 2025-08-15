from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.product_list, name="product_list"),
    path("p/<slug:slug>/", views.product_detail, name="product_detail"),
    path("fav/<slug:slug>/toggle/", views.toggle_favorite, name="toggle_favorite"),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<slug:slug>/", views.cart_add, name="cart_add"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("favorites/", shop_views.favorite_list, name="favorite_list"),
    path(
        "favorites/toggle/<slug:slug>/",
        shop_views.toggle_favorite,
        name="toggle_favorite",
    ),
    path("accounts/signup/", accounts_views.signup_view, name="signup"),
    path("cart/remove/<slug:slug>/", views.cart_remove, name="cart_remove"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
