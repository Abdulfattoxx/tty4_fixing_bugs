from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Product, Favorite, CartItem
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def _get_qty(request, default=1):
    val = request.POST.get("qty") or request.GET.get("qty") or default
    try:
        qty = int(val)
    except (TypeError, ValueError):
        qty = default
    return max(1, min(qty, 99))  # 1..99 oralig'ida


def _get_cart(session):
    return session.setdefault("cart", {})  # {slug: qty}


# ——— Catalog / Home ———
def product_list(request):
    q = request.GET.get("q", "")
    products = Product.objects.filter(is_active=True)
    if q:
        products = products.filter(name__icontains=q)

    fav_ids = set()
    if request.user.is_authenticated:
        fav_ids = set(
            Favorite.objects.filter(
                user=request.user, product__in=products
            ).values_list("product_id", flat=True)
        )

    return render(
        request,
        "shop/product_list.html",
        {"products": products, "q": q, "fav_ids": fav_ids},
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    is_fav = (
        request.user.is_authenticated
        and Favorite.objects.filter(user=request.user, product=product).exists()
    )
    return render(
        request, "shop/product_detail.html", {"product": product, "is_fav": is_fav}
    )


@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    is_fav = Favorite.objects.filter(user=request.user, product=product).exists()
    return render(
        request, "shop/product_detail.html", {"product": product, "is_fav": is_fav}
    )


# ——— Cart ———
def cart_view(request):
    items = []
    total = Decimal("0")

    if request.user.is_authenticated:
        # ✅ Login bo‘lsa — DB’dagi CartItem’larni ko‘rsatamiz
        qs = (CartItem.objects
              .select_related("product")
              .filter(user=request.user, product__is_active=True))
        for ci in qs:
            p = ci.product
            line_total = p.price * ci.qty
            items.append({"product": p, "qty": ci.qty, "line_total": line_total})
            total += line_total
    else:
        # ✅ Anonim bo‘lsa — sessiya savatchasi
        cart = _get_cart(request.session)  # {slug: qty}
        for slug, qty in cart.items():
            p = Product.objects.filter(slug=slug, is_active=True).first()
            if p:
                line_total = p.price * qty
                items.append({"product": p, "qty": qty, "line_total": line_total})
                total += line_total

    return render(request, "shop/cart.html", {"items": items, "total": total})



def cart_add(request, slug):
    p = get_object_or_404(Product, slug=slug, is_active=True)
    qty = _get_qty(request, default=1)

    if request.user.is_authenticated:
        item, created = CartItem.objects.get_or_create(user=request.user, product=p)
        item.qty = item.qty + qty if not created else qty
        item.save(update_fields=["qty"])
    else:
        cart = request.session.setdefault("cart", {})
        cart[slug] = int(cart.get(slug, 0)) + qty
        request.session.modified = True

    next_url = (
        request.GET.get("next")
        or request.POST.get("next")
        or request.META.get("HTTP_REFERER")
        or reverse("product_list")
    )
    return redirect(next_url)

def cart_remove(request, slug):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product__slug=slug).delete()
    else:
        cart = _get_cart(request.session)
        cart.pop(slug, None)
        request.session.modified = True
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or reverse("cart_view")
    return redirect(next_url)




# ——— Favorites ———
@login_required
def favorite_list(request):
    products = Product.objects.filter(favorite__user=request.user, is_active=True)
    fav_ids = set(products.values_list("id", flat=True))
    return render(
        request,
        "shop/favorite_list.html",
        {"products": products, "fav_ids": fav_ids, "q": ""},
    )


@login_required
def toggle_favorite(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    fav, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        fav.delete()
    next_url = (
        request.GET.get("next")
        or request.META.get("HTTP_REFERER")
        or reverse("product_list")
    )
    return redirect(next_url)


@require_POST
def cart_update(request, slug):
    qty = _get_qty(request, default=1)
    if request.user.is_authenticated:
        if qty <= 0:
            CartItem.objects.filter(user=request.user, product__slug=slug).delete()
        else:
            p = get_object_or_404(Product, slug=slug, is_active=True)
            item, _ = CartItem.objects.get_or_create(user=request.user, product=p)
            item.qty = qty
            item.save(update_fields=["qty"])
    else:
        cart = request.session.setdefault("cart", {})
        if qty <= 0:
            cart.pop(slug, None)
        else:
            cart[slug] = qty
        request.session.modified = True

    next_url = request.POST.get("next") or reverse("cart_view")
    return redirect(next_url)


def tg_app(request):
    # products + fav_ids tayyorlab berish (xuddi product_list'dagi kabi)
    q = request.GET.get("q", "")
    products = Product.objects.filter(is_active=True)
    if q:
        products = products.filter(description__icontains=q)  # yoki name__icontains
    fav_ids = set()
    if request.user.is_authenticated:
        fav_ids = set(Favorite.objects.filter(
            user=request.user, product__in=products
        ).values_list("product_id", flat=True))
    return render(request, "shop/tg_app.html", {"products": products, "fav_ids": fav_ids, "q": q})

@csrf_exempt
def tg_auth(request):
    return HttpResponse(status=204)