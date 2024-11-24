from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')  # 모든 게시글 조회
    serializer_class = PostSerializer  # PostSerializer 사용

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes += 1
        post.save()
        return Response({'status': 'like added', 'likes': post.likes})

