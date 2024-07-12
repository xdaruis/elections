from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
  ordering = ['id']
  list_display = ['username', 'email', 'name']
  fieldsets = (
    (None, {'fields': ('username', 'name', 'email')}),
    (
      _('Permissions'),
      {
        'fields': (
          'is_active',
          'is_staff',
          'is_superuser'
        )
      }
    ),
    (_('Important dates'), {'fields': ('last_login',)}),
  )
  readonly_fields = ['last_login']
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': (
        'username',
        'name',
        'email',
        'password1',
        'password2',
        'is_active',
        'is_staff',
        'is_superuser',
      )
    }),
  )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Election)
admin.site.register(models.Candidate)
admin.site.register(models.Vote)
