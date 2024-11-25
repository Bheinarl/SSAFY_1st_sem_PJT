from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import CustomUser

# 회원가입에 사용하는 CustomRegisterSerializer
class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    age = serializers.IntegerField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'password1', 'password2', 'age']
    
    def validate_nickname(self, value):
        if CustomUser.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("This nickname is already taken.")
        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            password=validated_data['password1'],
            age=validated_data.get('age', None)
        )
        return user


# 사용자 프로필을 가져올 때 사용할 CustomUserDetailsSerializer
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    max_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'nickname', 'age','my_investor_type', 'max_score')  # 필요한 필드를 직접 지정

    def get_age(self, obj):
        return obj.age if obj.age is not None else '비공개'

    def to_representation(self, instance):
        """ 디버깅을 위해 출력해 봄 """
        representation = super().to_representation(instance)
        print("User Representation:", representation)  # 콘솔에 출력
        return representation