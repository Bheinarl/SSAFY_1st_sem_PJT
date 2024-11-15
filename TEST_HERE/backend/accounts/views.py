from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  # 인증 없이 접근 가능하도록 권한 추가
from .serializers import CustomRegisterSerializer, CustomUserDetailsSerializer
from dj_rest_auth.views import UserDetailsView

class CustomRegisterView(APIView):
    permission_classes = [AllowAny]  # 인증 없이 접근 가능
    # CustomRegisterView에 AllowAny 권한을 설정하여, 인증되지 않은 사용자도 접근할 수 있도록 합니다. 회원가입 엔드포인트는 누구나 접근할 수 있어야 하므로 이 설정이 필요합니다.

    def post(self, request, *args, **kwargs):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer
    # CustomUserDetailsSerializer를 사용하도록 설정했습니다. 이는 프로필 정보에 nickname 필드를 포함하기 위함입니다.