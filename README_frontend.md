# Candy Shop Frontend

This repository includes a minimal Telegram WebApp front end for the Django Candy Shop backend.

## Run

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` inside Telegram WebView or normal browser.

## Pages

- `/` – home, product list
- `/search/` – search products
- `/categories/` – categories list
- `/cart/` – cart view
- `/favorites/` – favorite products
- `/profile/` – user profile
- `/accounts/login/` – email login
- `/accounts/signup/` – registration

## Manual smoke test

1. Home page loads and shows products.
2. Search page returns filtered products.
3. Categories list is accessible from bottom navigation.
4. Favorite toggle updates badge.
5. Add to cart updates cart badge and cart totals.
6. Cart page supports quantity +/- and removal.
7. Login/Logout redirects correctly and profile shows email.
8. Theme changes from Telegram update colors.
