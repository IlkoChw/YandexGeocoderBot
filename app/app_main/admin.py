from django.contrib import admin
from .models import BotUser, SearchArea, SearchResult
from django.conf import settings


admin.site.site_header = settings.APP_NAME
admin.site.enable_nav_sidebar = False


class BotUserRequestsInline(admin.StackedInline):
    model = SearchResult


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    inlines = (BotUserRequestsInline, )


@admin.register(SearchArea)
class SearchAreaAdmin(admin.ModelAdmin):
    list_display = ('__str__', )


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'created')
    list_filter = ('created', )





