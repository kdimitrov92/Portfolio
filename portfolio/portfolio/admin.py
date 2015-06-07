from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as OriginalGroupAdmin
from django.contrib.auth.models import Group, User as AuthUser
from django.contrib.auth.models import Permission

from portfolio.models.photos import Album, Photo
from portfolio.models.blogs import Blog
from portfolio.models.comments import PhotoComment, BlogComment


class MembershipInline(admin.TabularInline):
    model = AuthUser.groups.through
    raw_id_fields = ('user',)


class GroupAdmin(OriginalGroupAdmin):
    inlines = (MembershipInline,)

    class Media:
        css = {'all': ('css/hide_admin_original.css',)}


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')
    list_filter = ('content_type',)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class PhotoCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'content')


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'content')


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(PhotoComment, PhotoCommentAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
