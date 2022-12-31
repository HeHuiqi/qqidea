from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.db.models.query import QuerySet

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. 用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner的字段
    2. 用户针对query set过滤当前用户的数据
    """
    # 排除字段
    exclude = ['owner']

    # 过滤当前用户才能看到的内容
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).filter(owner=request.user)
    
    # 重写这个方法可以在save()之前做一些处理操作
    def save_model(self, request: HttpRequest, obj: Any, form: Any, change: Any):
        # request.user 就是管理后台当前登录的用户
        obj.owner = request.user
        return super().save_model(request, obj, form, change)