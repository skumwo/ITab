from django.contrib import admin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role',)
    actions = ['make_admin']

    def make_admin(self, request, queryset):
        for user in queryset:
            if not user.is_superuser:  # Чтобы не трогать суперпользователей
                user.role = 'admin'
                user.is_staff = True
                user.save()
    make_admin.short_description = "Give selected users admin rights"

admin.site.register(User, CustomUserAdmin)
