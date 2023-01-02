from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','category','description','content','content_html','created_time']