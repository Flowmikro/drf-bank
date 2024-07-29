from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserModel
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    """Admin panel for CustomUser"""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserModel
    list_display = ("id", "email", "is_staff", "is_active",)
    list_filter = ("id", "email",)
    fieldsets = (
        (None, {"fields": ("email", "password", "balance", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = ("date_joined",)


admin.site.register(UserModel, CustomUserAdmin)
