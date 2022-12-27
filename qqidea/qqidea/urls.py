
from django.contrib import admin
from django.urls import path,re_path

from blog.views import post_list,post_detail
from config.views import links

from .custom_site import custom_site

urlpatterns = [

    # 使用自定义的管理后台
    path('', view=post_list),
    path('category/<category_id>/',view=post_list),
    path('tag/<tag_id>/',view=post_list),
    path('post/<post_id>.html/',view=post_detail),
    path('links/',view=links),

    path('supper_admin/', admin.site.urls,name='supper_admin'),
    # 使用自定义的管理后台
    path('admin/', custom_site.urls,name='custom_admin'),

]
