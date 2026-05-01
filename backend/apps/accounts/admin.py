from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    BaseUserCreationForm,
    UserChangeForm,
    UsernameField,
)
from django.utils.translation import gettext_lazy as _

from .models import OTP, User


class AdminUserCreationForm(BaseUserCreationForm):
    """Hashes password via set_password on save (default ModelAdmin does not)."""

    class Meta:
        model = User
        fields = ("email", "phone_number")
        field_classes = {"email": UsernameField}


class AdminUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        field_classes = {"email": UsernameField}


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    change_password_form = AdminPasswordChangeForm

    ordering = ("email",)
    list_display = ("email", "phone_number", "is_staff", "is_active", "created_at")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "phone_number")
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("phone_number", "first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2"),
            },
        ),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "is_used", "created_at")
    search_fields = ("phone_number",)
