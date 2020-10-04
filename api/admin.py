from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "bio",
        "email",
        "role",
        "confirmation_code",
    )
    search_fields = ("username",)
    list_filter = ("username",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
