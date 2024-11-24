from .models import Post
from .serializers import PostSerializer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Post
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

# 게시글 목록 조회
@csrf_exempt
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')  # 모든 게시글 조회
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

# 게시글 작성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request):
    try:
        # request.data는 Django Rest Framework가 자동으로 JSON을 파싱
        serializer = PostSerializer(data=request.data, context={'request': request})  # context에 request 포함
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # 오류 메시지 출력
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세 보기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    serializer = PostSerializer(post)
    return Response(serializer.data)

# 게시글 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return Response({"error": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return Response({"error": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    post.delete()
    return Response({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# 좋아요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # 이미 좋아요를 눌렀으면 좋아요 취소
    if user in post.liked_users.all():
        post.liked_users.remove(user)
        post.likes -= 1
        post.save()
        return Response({"message": "좋아요가 취소되었습니다."}, status=status.HTTP_200_OK)
    
    # 좋아요를 누르지 않았으면 좋아요 추가
    post.likes += 1
    post.liked_users.add(user)
    post.save()
    return Response({"message": "좋아요가 추가되었습니다."}, status=status.HTTP_200_OK)