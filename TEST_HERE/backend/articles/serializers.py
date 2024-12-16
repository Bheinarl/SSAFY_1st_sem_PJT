from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # 댓글 작성자 이름 표시
    author_username = serializers.SerializerMethodField()  # 댓글 작성자의 username
    author_profile_picture = serializers.SerializerMethodField()  # 작성자 프로필 사진 표시

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_username', 'author_profile_picture', 'content', 'created_at']
    
    def get_author_username(self, obj):
        return obj.author.username

    def get_author_profile_picture(self, obj):
        request = self.context.get('request', None)
        if obj.author.profile_picture and request:
            return request.build_absolute_uri(obj.author.profile_picture.url)
        return request.build_absolute_uri('/static/images/default-user.png')  # 기본 이미지 URL 반환


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # 작성자 이름 표시
    author_profile_picture = serializers.SerializerMethodField()  # 작성자 프로필 사진 표시
    likes = serializers.ReadOnlyField()  # 좋아요 수 읽기 전용
    liked_users = serializers.StringRelatedField(many=True, read_only=True)  # 좋아요 누른 사용자 표시

    class Meta:
        model = Post  # Post(게시물) 모델을 사용
        fields = ['id', 'title', 'content', 'likes', 'author', 'author_profile_picture', 'liked_users', 'created_at']

        # 작성자, 좋아요를 누른 사용자 목록, 수정일자, 작성일자는 읽기 전용 필드로 설정
        read_only_fields = ['author', 'liked_users', 'updated_at', 'created_at']
    
    def get_author(self, obj):
        return obj.author.username  # 작성자 이름 반환

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user  # 현재 로그인한 사용자를 글쓴이로 지정
        return super().create(validated_data)

    def get_author_profile_picture(self, obj):
        request = self.context.get('request', None)  # 요청 객체 가져오기
        if obj.author.profile_picture:
            return request.build_absolute_uri(obj.author.profile_picture.url)
        return request.build_absolute_uri('/static/images/default-user.png')