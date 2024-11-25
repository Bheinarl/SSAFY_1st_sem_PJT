from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import CustomUser

# 회원가입에 사용하는 CustomRegisterSerializer
class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)  # 비밀번호 필드 추가
    password2 = serializers.CharField(write_only=True)  # 비밀번호 확인 필드 추가
    age = serializers.IntegerField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'password1', 'password2', 'age']
    
    def validate_nickname(self, value):  # nickname 필드에 대한 유효성 검사
        if CustomUser.objects.filter(nickname=value).exists():  # 이미 존재하는 nickname인지 확인
            raise serializers.ValidationError("This nickname is already taken.")
        return value

    def validate(self, data):  # password1과 password2가 같은지 확인
        if data['password1'] != data['password2']:  # 같지 않으면 에러 발생
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):  # 유저 생성
        validated_data.pop('password2')  # password2 필드는 사용하지 않으므로 삭제
        user = CustomUser.objects.create_user(
            username=validated_data['username'],  
            nickname=validated_data['nickname'],  
            password=validated_data['password1'],  
            age=validated_data.get('age', None)
        )
        return user


# 사용자 프로필을 가져올 때 사용할 CustomUserDetailsSerializer
class CustomUserDetailsSerializer(serializers.ModelSerializer):  # UserDetailsSerializer를 상속받아서 사용
    username = serializers.CharField(read_only=True)  # username 필드를 읽기 전용으로 설정
    max_score = serializers.IntegerField(read_only=True)  # max_score 필드를 읽기 전용으로 설정

    class Meta:
        model = CustomUser
        fields = ('username', 'nickname', 'age','my_investor_type', 'max_score')  # 필요한 필드를 직접 지정

    def get_age(self, obj):  # age 필드를 가져올 때 None이면 '비공개'로 반환
        return obj.age if obj.age is not None else '비공개'

    def to_representation(self, instance):
        """ 디버깅을 위해 출력해 봄 """
        representation = super().to_representation(instance)
        print("User Representation:", representation)  # 콘솔에 출력
        return representation