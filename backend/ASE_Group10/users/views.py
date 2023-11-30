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