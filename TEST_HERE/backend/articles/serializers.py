from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # 작성자 이름 표시

    class Meta:
        model = Post
        # fields = ['id', 'title', 'content', 'likes', 'author', 'created_at']
        fields = ['id', 'title', 'content', 'likes', 'author', 'created_at']
