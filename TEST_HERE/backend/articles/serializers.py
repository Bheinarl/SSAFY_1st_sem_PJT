from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # 작성자 이름 표시
    likes = serializers.ReadOnlyField()  # 좋아요 수 읽기 전용

    class Meta:
        model = Post
        # fields = ['id', 'title', 'content', 'likes', 'author', 'created_at']
        fields = ['id', 'title', 'content', 'likes', 'author', 'created_at']
        read_only_fields = ['author', 'updated_at', 'created_at']  # 수정일자, 작성일자는 읽기 전용
    
    def get_author(self, obj):
        return obj.author.username  # 작성자 이름 반환

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user  # 현재 로그인한 사용자를 글쓴이로 지정
        return super().create(validated_data)
