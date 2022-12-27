from typing import Any
from django.contrib import admin

from qqidea.custom_site import custom_site
from qqidea.base_admin import BaseOwnerAdmin


from .models import Link,SideBar

@admin.register(Link,site=custom_site)
# class LinkAdmin(admin.ModelAdmin):
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title','href','status','weight','created_time')
    fields = ['title','href','status','weight']

    def save_model(self, request: Any, obj: Link, form: Any, change: Any) -> None:
        obj.owner = request.user
        return super(LinkAdmin,self).save_model(request, obj, form, change)

@admin.register(SideBar,site=custom_site)
# class SidebarAdmin(admin.ModelAdmin):
class SidebarAdmin(BaseOwnerAdmin):
    list_display = ('title','display_type','content','created_time')
    fields = ['title','display_type','content']

    def save_model(self, request: Any, obj: SideBar, form: Any, change: Any) -> None:
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

