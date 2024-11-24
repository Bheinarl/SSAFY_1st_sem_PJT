from .models import Post
from .serializers import PostSerializer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')  # 모든 게시글 조회
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request):
    try:
        data = json.loads(request.body)  # JSON 데이터 파싱
        # data['author'] = request.user.id  # 현재 로그인한 사용자를 글쓴이로 지정
        serializer = PostSerializer(data=data, context={'request': request})  # context에 request 포함
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)