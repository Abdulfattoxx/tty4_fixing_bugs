# shop/admin.py
from django.contrib import admin
from django import forms
from .models import Category, Product, Favorite

try:
    from .models import CartItem
except Exception:
    CartItem = None


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("image"):
            raise forms.ValidationError("Rasm majburiy.")
        if not cleaned.get("category"):
            raise forms.ValidationError("Kategoriya majburiy.")
        desc = (cleaned.get("description") or "").strip()
        if not desc:
            raise forms.ValidationError("Tavsif (description) majburiy.")
        return cleaned


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "category", "price", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    list_select_related = ("user", "product")


if CartItem:

    @admin.register(CartItem)
    class CartItemAdmin(admin.ModelAdmin):
        list_display = ("user", "product", "qty", "added_at")
        list_select_related = ("user", "product")
