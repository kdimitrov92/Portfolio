from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as OriginalGroupAdmin
from django.contrib.auth.models import Group, User as AuthUser
from django.contrib.auth.models import Permission


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


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission, PermissionAdmin)
