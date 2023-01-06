from django.urls import reverse
from rest_framework import serializers,pagination


from .models import Post,Category


    
# 指定序列化字段的格式
class PostSerializer(serializers.ModelSerializer):

    # 外建数据
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    # 外建数据，many=True表示多对多关系，slug_field展示关系模型的字段
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    # 外建数据
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time = serializers.DateTimeField(
        read_only=True,
        format='%Y-%m-%d %H:%M:%S' 
    )
    # 增加一个字段
    url = serializers.CharField(
        read_only=True,
        default='http://',
    )
    class Meta:
        model = Post
        fields = ['id','title','category','tag','owner','created_time','url']
        extra_kwargs ={
        # 指定read_only为True, max_value为9999, min_value为0
            "readcount": {"read_only": True, "max_value": 9999, "min_value": 0},
             "commentcount": {"max_value": 9999, "min_value": 0}
        }


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id','title','category','tag','owner','description','content','content_html','created_time']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','created_time']

class CategoryDetailSerializer(CategorySerializer):
    # 将 posts 字段的数据映射到 paginated_posts 的方法的返回值上
    posts = serializers.SerializerMethodField('paginated_posts')
    def paginated_posts(self,obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        # 初始化分页
        paginator = pagination.PageNumberPagination()
        # 必须指定size
        paginator.page_size = 2
        page = paginator.paginate_queryset(posts,self.context['request'])
        # serializer = PostSerializer(page,many=True,context={'request':self.context['request']})
        serializer = PostDetailSerializer(page,many=True,context={'request':self.context['request']})

        return {
            'count':len(posts),
            'page_size':paginator.page_size,
            'result':serializer.data,
            'previous':paginator.get_previous_link(),
            'next':paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = ['id','name','created_time','posts']