
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.db.models.query import QuerySet

from django.contrib.admin.models import LogEntry


from qqidea.custom_site import custom_site
# 使用基类
from qqidea.base_admin import BaseOwnerAdmin

from .models import Post,Category,Tag
from .adminforms import PostAdminForm




# StackedInline 垂直排列字段
# TabularInline 水平排列字段
class PostInline(admin.StackedInline):
    fields = ['title','description']
    extra = 1
    model = Post
    

# @admin.register(Category)
@admin.register(Category,site=custom_site)
# class CategoryAdmin(admin.ModelAdmin):
class CategoryAdmin(BaseOwnerAdmin):
    # 用户管理后台列表页面显示的字段
    list_display = ('name','status','is_nav','created_time','post_count')
    # 用户管理后 在保存或修改model要填写的字段
    fields = ('name','status','is_nav')
    # 直接在博客分类下编辑文章的一些操作
    # inlines = [PostInline]

    # 重写这个方法可以在save()之前做一些处理操作
    # def save_model(self, request: HttpRequest, obj: Category, form: Any, change: Any) -> None:
    #     # 设置分类的作者为当前登录的用户
    #     # request.user 就是管理后台当前登录的用户
    #     obj.owner = request.user
    #     return super().save_model(request, obj, form, change)

    #自定义字段,展示该分类先有多少文章
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

# @admin.register(Tag)
@admin.register(Tag,site=custom_site)
# class TagAdmin(admin.ModelAdmin):
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    # def save_model(self, request: HttpRequest, obj: Category, form: Any, change: Any) -> None:
    #     obj.owner = request.user
    #     return super().save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    title = '分类过滤器'
    parameter_name = 'owner_category'
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        # print('category_id=',category_id)
        # print('queryset=',queryset)

        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


# @admin.register(Post)
@admin.register(Post,site=custom_site) #使用自定义的管理后台
# class PostAdmin(admin.ModelAdmin):
class PostAdmin(BaseOwnerAdmin):
    list_display = [
        'id','title','category','status','owner','pv','uv',
        'created_time','operator'
    ]
    # 配置哪些字段可以作为链接点击进入编辑页面
    list_display_links = []
    # 配置过滤字段
    # list_filter = ['category']
    list_filter = (CategoryOwnerFilter,)

    # 配置搜索字段在列表页显示
    search_fields = ['title','category__name']
    # 动作相关的是否显示在顶部
    actions_on_top = True
    # 动作相关的是否显示在底部
    actions_on_bottom = True

    #增加、编辑、保存是否在顶部也显示
    save_on_top = True

    # 简单的罗列要提交的字段
    # fields = [
    #     ('category','title'),
    #     'description',
    #     'status',
    #     'content',
    #     'tag',
    # ]

    # 分区显示字段和fields属性只能指定其一
    fieldsets = [
        ('基础配置',{'description':'基础配置的字段描述','fields':('title','category','status',),}),
        ('内容',{'fields':('description','content')}),
        # classses 的作用是给配置添加一些CSS属性,默认支持collapse和wide
        ('选择标签',{'classes':('wide',),'fields':('tag',)}),
    ]
    # 配置自定义的form
    form = PostAdminForm
    # 对于多对多关系可以设置过滤样式
    filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    # 自定义字段
    def operator(self,obj):
        return format_html('<a href="./{}/change/">编辑</a>'.format(obj.id))
    operator.short_description = '操作'


    # def save_model(self, request: HttpRequest, obj: Post, form: Any, change: Any) -> None:
    #     obj.owner = request.user
    #     return super().save_model(request, obj, form, change)

    # def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
    #     # 仅显示当前用户的文章
    #     return super(PostAdmin,self).get_queryset(request).filter(owner=request.user)

    # 配置自己的css和js,然后我们就可以指定我们的css了
    # class Media:
    #     css= {'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",)}
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


# 自定义变更日志显示
@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']