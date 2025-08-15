"""candyshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop import views as shop_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # shop
    path("", shop_views.product_list, name="product_list"),
    path("search/", shop_views.search_view, name="search"),
    path("categories/", shop_views.categories_view, name="categories"),
    path("p/<slug:slug>/", shop_views.product_detail, name="product_detail"),
    path("fav/<slug:slug>/toggle/", shop_views.toggle_favorite, name="toggle_favorite"),
    path("cart/", shop_views.cart_view, name="cart_view"),
    path("cart/add/<slug:slug>/", shop_views.cart_add, name="cart_add"),
    path("cart/remove/<slug:slug>/", shop_views.cart_remove, name="cart_remove"),
    path("cart/update/<slug:slug>/", shop_views.cart_update, name="cart_update"),
    path("favorites/", shop_views.favorite_list, name="favorite_list"),
    path("profile/", shop_views.profile_view, name="profile"),
    # API endpoints
    path("api/auth/me/", shop_views.auth_me, name="auth_me"),
    path("api/favorites/toggle/", shop_views.favorites_toggle_api, name="favorites_toggle_api"),
    path("api/cart/add/", shop_views.cart_add_api, name="cart_add_api"),
    path("api/cart/update/", shop_views.cart_update_api, name="cart_update_api"),
    path("api/cart/remove/", shop_views.cart_remove_api, name="cart_remove_api"),
    path("tg/app/",  shop_views.tg_app,  name="tg_app"),
    path("tg/auth/", shop_views.tg_auth, name="tg_auth"),
    # auth (login/logout/password pages)
    path("accounts/", include("django.contrib.auth.urls")),
    # signup (o'zimizniki)
    path("accounts/", include("accounts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
