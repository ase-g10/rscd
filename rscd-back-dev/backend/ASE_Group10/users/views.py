from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if user.verify_password(password):
                # 密码正确
                return Response({"message": "登录成功"}, status=status.HTTP_200_OK)
            else:
                # 密码错误
                return Response({"message": "无效的用户名或密码"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # 用户不存在
            return Response({"message": "无效的用户名或密码"}, status=status.HTTP_400_BAD_REQUEST)
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        # 从请求中获取注册信息
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            # 检查用户是否已经存在
            existing_user = User.objects.get(username=username)
            return Response({"message": "该用户名已被注册"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # 创建新用户
            new_user = User(username=username)
            new_user.set_password(password)
            new_user.save()

            return Response({"message": "注册成功"}, status=status.HTTP_200_OK)