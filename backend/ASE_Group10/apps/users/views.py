from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            # 这里可以返回用户的某种认证令牌或者其他相关信息
            return Response({"message": "登录成功"}, status=status.HTTP_200_OK)
        return Response({"message": "无效的用户名或密码"}, status=status.HTTP_400_BAD_REQUEST)
