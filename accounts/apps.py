from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "User Accounts"

    def ready(self):
        # Agar signals ishlatsang, shu yerda import qilasan
        # from . import signals
        pass
