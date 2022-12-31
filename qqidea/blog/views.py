from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,HttpResponse,get_object_or_404


from .models import Post,Category,Tag,User
from config.models import SideBar,Link
from comment.models import Comment
from comment.forms import CommentForm


def post_list(request,category_id=None,tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list,tag = Post.get_by_tag(tag_id=tag_id)    
    elif category_id:
        post_list,category = Post.get_by_category(category_id=category_id)
    else:
        post_list = Post.latest_posts()
        # print('post_list:',post_list)
    template_name = 'blog/list.html'
    context = {
        'category':category,
        'tag':tag,
        'post_list':post_list,
        'sidebars':SideBar.get_all()

    }
    # 增加分类数据
    context.update(Category.get_navs())
    return render(request=request,template_name=template_name,context=context)

def post_detail(request,post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    
    template_name = 'blog/detail.html'
    context = {
        'post':post,
        'sidebars':SideBar.get_all()
    }
     # 增加分类数据
    context.update(Category.get_navs())
    return render(request=request,template_name=template_name,context=context)

# 使用CBV重构

from django.views.generic import ListView,DetailView

class CommonViewMixin:
    # 传递给模版的上下文数据
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        #  将侧边栏数据和分类的导航数据设置到上下文中
        context.update({
            'sidebars':SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context

class IndexView(CommonViewMixin,ListView):
    queryset = Post.latest_posts()
    # 每页大小
    paginate_by = 5
    # 传递给模版的变量名称
    context_object_name = 'post_list'
    # 使用的模版名
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update({
            'category':category
        })
        return context

    def get_queryset(self) -> QuerySet[Any]:
        quryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return quryset.filter(category_id = category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag,pk=tag_id)
        context.update({
            'tag':tag
        })
        return context

    def get_queryset(self) -> QuerySet[Any]:
        quryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return quryset.filter(tag__id = tag_id)

class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form':CommentForm,
            'comment_list':Comment.get_by_target(self.request.path)
        })
        return context

# 搜索文章
from django.db.models import Q
class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({'keyword':self.request.GET.get('keyword','')})
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset =  super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        # Q()条件查询，这里查询标题和摘要描述包含keyword的文章
        # 只需要知道，通过Q表达式实现了类似这样的SQL语句: 
        # SELECT ★FROM post WHERE title LIKE '%<keyword>%' or description ILIKE '%<keyword>%'
        return queryset.filter(Q(title__icontains=keyword)|Q(description__icontains=keyword))
    
# 查询某个作者的所有文章
class AuthorPostListView(IndexView):
    def get_queryset(self) -> QuerySet[Any]:
        quryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return quryset.filter(owner_id=author_id)


