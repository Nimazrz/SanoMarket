from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address
from .forms import *


class AddressInLine(admin.TabularInline):
    model = Address
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ['-created_at']
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['phone', 'first_name', 'last_name', 'is_staff', 'is_active', ]
    list_editable = ['is_staff', ]
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'national_code')}),
        ('Permissions', {'fields': (
             'is_seller', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'is_seller', 'national_code')}),
    )
    inlines = [AddressInLine]
