from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import UserAccount

User = get_user_model()


class UserAccountInline(admin.StackedInline):
    model = UserAccount
    can_delete = False
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    inlines = (UserAccountInline,)


# xavfsiz unregister
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
