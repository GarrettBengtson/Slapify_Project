from django.contrib import admin
from .models import User, Song, Playlist, UserRequest, AdminEdit
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(UserRequest)
admin.site.register(AdminEdit)