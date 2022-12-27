from django.shortcuts import render,HttpResponse

from .models import Post,Tag

def post_list(request,category_id=None,tag_id=None):
    content = 'post list category_id={category_id},tag_id={tag_id}'.format(
        category_id = category_id,
        tag_id = tag_id
    )
  
    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    else:
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            post_list = Post.objects.filter(category_id=category_id)
    template_name = 'blog/list.html'
    context = {
        'post_list':post_list
    }
    return render(request=request,template_name=template_name,context=context)
def post_detail(request,post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    
    template_name = 'blog/detail.html'
    context = {
        'post':post
    }
    return render(request=request,template_name=template_name,context=context)

