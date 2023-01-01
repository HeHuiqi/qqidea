
from django.contrib import admin
from django.urls import path,re_path

from blog.views import post_list,post_detail
from blog.views import IndexView,CategoryView,TagView,PostDetailView,SearchView,AuthorPostListView
from config.views import links,LinkListView
from comment.views import CommentView

from .custom_site import custom_site

# rss 和 sitemap
from django.contrib.sitemaps import views as sitemap_vews
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap

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

    path('search/',view=SearchView.as_view(),name='search'),

    path('author/<owner_id>/',view=AuthorPostListView.as_view(),name='author'),


    path('links/',view=LinkListView.as_view(),name='links'),

    path('comment/',view=CommentView.as_view(),name='comment'),

    # rss 和 sitemap
    path('rss/',view=LatestPostFeed(),name='rss'),
    path('sitemap.xml',view=sitemap_vews.sitemap,kwargs={'sitemaps':{'posts':PostSitemap}}),


    path('supper_admin/', admin.site.urls,name='supper_admin'),
    # 使用自定义的管理后台
    path('admin/', custom_site.urls,name='custom_admin'),

]
