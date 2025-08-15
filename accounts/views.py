# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages


def signup(request):
    next_url = request.GET.get("next")  # ixtiyoriy: qaytish manzili
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # avtomatik login
            messages.success(
                request, "Tabriklaymiz! Ro‘yxatdan muvaffaqiyatli o‘tdingiz."
            )
            return redirect(next_url or "product_list")
    else:
        form = UserCreationForm()
    # Use new shop template
    return render(request, "shop/signup.html", {"form": form})
