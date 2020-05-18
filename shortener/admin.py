from django.contrib import admin
from user.admin import admin_site
from shortener.models import  URL

# Register your models here.
admin_site.register(URL)