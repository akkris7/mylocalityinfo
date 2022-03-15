from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = [
        'id',
        'email',
        'name', 
        'location',
        'is_admin',
        'is_superuser'
    ]
    list_filter = ['name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'mobile', 'location', 'profile_pic')}),
        ('Permissions', {'fields': ('is_superuser', 'is_admin', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password',
                'password_2',
                'name', 
                'mobile',
                'location',
                'is_active',
                'is_superuser',
                'is_staff',
                'is_admin', 
                'groups',
                'user_permissions',
                'profile_pic'
            )}
        ),
    )
    search_fields = ['email', 'name']
    ordering = ['email', 'name']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)