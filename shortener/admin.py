from django.contrib import admin
from shortener.models import URL, Transition


# Register your models here.
class URLAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_link', 'short_link_with_hostname')


class TransitionAdmin(admin.ModelAdmin):
    list_display = (
        'url_creator', 'url_title', 'url_full_link', 'transition_datetime', 'ip', 'country', 'region', 'city'
    )

    def url_title(self, obj):
        return obj.url.title
    url_title.short_description = 'Название'

    def url_creator(self, obj):
        return obj.url.owner
    url_creator.short_description = 'Создатель URL'

    def url_full_link(self, obj):
        return obj.url.full_link
    url_full_link.short_description = 'Полная ссылка'


admin.site.register(URL, URLAdmin)
admin.site.register(Transition, TransitionAdmin)
