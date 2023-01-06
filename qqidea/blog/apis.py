from rest_framework import generics,viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination,CursorPagination

from .models import Post,Category
from .serializers import (
    PostSerializer,PostDetailSerializer,
    CategorySerializer,
    CategoryDetailSerializer,
)



@api_view(http_method_names=['get'])
def api_post_list(request):
    posts =Post.objects.filter(status=Post.STATUS_NORMAL)
    post_serializers = PostSerializer(posts,many=True)
    return Response(post_serializers.data)

# 定义分页类1
class QiLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2

# 定义分页类2 
class QiCursorrPagination(CursorPagination):
    page_size = 3
    # 必须指定排序字段
    ordering = '-created_time'
    pass

# 定义分页类3 
class QiPageNumberPagination(PageNumberPagination):
    page_size = 2


# 允许get和post请求
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer
    pagination_class = QiPageNumberPagination

# viewsets.ModelViewSet 允许 post get put delete 请求,可根据情况继承不同的ViewSet
# class ModelViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet)

# 仅允许get请求
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Post.objects.filter(status = Post.STATUS_NORMAL)
    def get_queryset(self):
        queryset = Post.objects.filter(status = Post.STATUS_NORMAL)
        return queryset

    serializer_class = PostSerializer

    # 配置分页
    # pagination_class = QiLimitOffsetPagination
    # pagination_class = QiCursorrPagination
    pagination_class = QiPageNumberPagination

    

    # 这是获取单一对象时的方法
    def retrieve(self, request, *args, **kwargs):
        # 这里指定博客详情的序列化类
        self.serializer_class = PostDetailSerializer

        # return super().retrieve(request, *args, **kwargs)

        instance:Post = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['address'] = '中国'
        # 增加返回数据
        rspData = {
            'status':'success',
            'data':data
        }
        return Response(data=rspData)

    
    def filter_queryset(self, queryset):
        print('self.request.query_params:',self.request.query_params)
        # http://127.0.0.1:8000/api/post/?category=1
        category_id = self.request.query_params.get('category')
        print('category_id:',category_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    pagination_class = QiPageNumberPagination

     # 这是获取单一对象时的方法
    def retrieve(self, request, *args, **kwargs):
        # 这里指定分类详情的序列化类
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)