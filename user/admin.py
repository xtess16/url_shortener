from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as _UserAdmin, GroupAdmin

from user.models import User, UserGroup


class UserSite(AdminSite):
    site_title = 'URL Shortener'
    site_header = 'URL-S'


admin_site = UserSite()
admin.site = admin_site


class UserAdmin(_UserAdmin):
    pass


admin_site.register(User, UserAdmin)
admin_site.register(UserGroup, GroupAdmin)
