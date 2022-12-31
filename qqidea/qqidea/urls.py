
from django.contrib import admin
from django.urls import path,re_path

from blog.views import post_list,post_detail
from blog.views import IndexView,CategoryView,TagView,PostDetailView
from config.views import links

from .custom_site import custom_site

urlpatterns = [

    # 使用自定义的管理后台
    # path('', view=post_list,name='index'),
    path('', view=IndexView.as_view(),name='index'),

    # path('category/<category_id>/',view=post_list,name='category-list'),
    path('category/<category_id>/',view=CategoryView.as_view(),name='category-list'),


    # path('tag/<tag_id>/',view=post_list,name='tag-list'),
    path('tag/<tag_id>/',view=TagView.as_view(),name='tag-list'),

    # path('post/<post_id>.html/',view=post_detail,name='post-detail'),
    path('post/<post_id>.html/',view=PostDetailView.as_view(),name='post-detail'),


    path('links/',view=links,name='links'),

    path('supper_admin/', admin.site.urls,name='supper_admin'),
    # 使用自定义的管理后台
    path('admin/', custom_site.urls,name='custom_admin'),

]
