
from django.contrib import admin
from django.urls import path,re_path,include

from django.conf import settings
from blog.views import post_list,post_detail
from blog.views import IndexView,CategoryView,TagView,PostDetailView,SearchView,AuthorPostListView
from config.views import links,LinkListView
from comment.views import CommentView



from .custom_site import custom_site

# rss 和 sitemap
from django.contrib.sitemaps import views as sitemap_vews
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap

# api
from rest_framework.routers import DefaultRouter
from blog.apis import api_post_list,PostList,PostViewSet,CategoryViewSet
# 配置 api 文档
from rest_framework.documentation import include_docs_urls


router =DefaultRouter()
#使用 PostViewSet view  我们定义了 /api/post/ 和 /api/post/1/ 两个api
router.register(r'post',PostViewSet,basename='api-post')
# 我们定义了 /api/category/ 和 /api/category/1/ 两个api
router.register(r'category',CategoryViewSet,basename='api-category')


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
    # http://127.0.0.1:8000/rss/
    path('rss/',view=LatestPostFeed(),name='rss'),

    # http://127.0.0.1:8000/sitemap.xml
    path('sitemap.xml',view=sitemap_vews.sitemap,kwargs={'sitemaps':{'posts':PostSitemap}}),


    # http://127.0.0.1:8000/api/post/
    #api
    # path('api/post/',view=api_post_list,name='post-list'),
    # path('api/post/',view=PostList.as_view(),name='post-list'),

    # http://127.0.0.1:8000/api/
    # http://127.0.0.1:8000/api/post/
    # http://127.0.0.1:8000/api/post/1
    path('api/',include((router.urls,'api'),namespace='api')),

    # 定义api文档路由
    # http://127.0.0.1:8000/api/docs/
    path("api/docs/",include_docs_urls(title='qqidea api')),


    path('supper_admin/', admin.site.urls,name='supper_admin'),
    # 使用自定义的管理后台
    path('admin/', custom_site.urls,name='custom_admin'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]


