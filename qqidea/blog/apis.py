from rest_framework import generics,viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer

@api_view(http_method_names=['get'])
def api_post_list(request):
    posts =Post.objects.filter(status=Post.STATUS_NORMAL)
    post_serializers = PostSerializer(posts,many=True)
    return Response(post_serializers.data)

# 定义了get和post方法
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status = Post.STATUS_NORMAL)
    serializer_class = PostSerializer
