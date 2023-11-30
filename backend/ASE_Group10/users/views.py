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
            # 从数据库中查找用户
            user = User.objects.get(username=username)

            # 检查提供的密码是否与存储的密码匹配
            if password == user.password:
                # 如果密码匹配，返回成功消息
                return Response({"message": "登录成功"}, status=status.HTTP_200_OK)
            else:
                # 如果密码不匹配，返回错误消息
                return Response({"message": "无效的用户名或密码"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            # 如果没有找到用户，返回错误消息
            return Response({"message": "无效的用户名或密码"}, status=status.HTTP_400_BAD_REQUEST)
