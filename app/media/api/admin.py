from django.contrib import admin
from .models import Account, Media, Album, MediaTag, AlbumTag


class AccountAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email', 'country')
    fields = ('first_name', 'last_name', 'email', 'country', 'account_settings')
    list_display = ('first_name', 'email', 'country')


class MediaTagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    fields = ('name',)
    list_display = ('name',)


class MediaAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'tags__name')
    list_display = ('title', 'hidden')
    fields = ('title', 'description', 'src', 'hidden', 'tags')


class AlbumTagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    fields = ('name',)
    list_display = ('name',)


class AlbumAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'owner', 'tags__name')
    list_display = ('title', 'owner', 'access_level')
    fields = ('title', 'description', 'owner', 'access_level', 'unlisted', 'tags__name')


admin.site.register(Account, AccountAdmin)
admin.site.register(MediaTag, MediaTagAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(AlbumTag, AlbumTagAdmin)
admin.site.register(Album, AlbumAdmin)

