import requests
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from social_core.exceptions import AuthException
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from models.models import User


class Authentication(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password or not email:
            print("Username, email and password are required")
            return Response({"error": "Username, email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        print(f'User {user.username} created')
        user.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class Auth2(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def redirect_to_github(self, request):
        github_login_url = f"https://github.com/login/oauth/authorize?client_id={settings.SOCIAL_AUTH_GITHUB_KEY}&redirect_uri={settings.SOCIAL_AUTH_GITHUB_REDIRECT_URI}"
        return redirect(github_login_url)

    @action(detail=False, methods=['get'])
    def github_callback(self, request):
        # 从 GitHub 重定向回来的临时代码
        try:
            code = request.GET.get('code')
            if code:
                # 向 GitHub 请求 access token
                token_response = requests.post(
                    'https://github.com/login/oauth/access_token',
                    data={
                        'client_id': settings.SOCIAL_AUTH_GITHUB_KEY,
                        'client_secret': settings.SOCIAL_AUTH_GITHUB_SECRET,
                        'code': code,
                    },
                    headers={'Accept': 'application/json'}
                )
                token_json = token_response.json()
                access_token = token_json.get('access_token')

                # 使用 access token 获取用户信息等
                # TODO: LOGIN SUCCESSFUL/FAILURE/UPDATE USER INFO/CREATE USER
                # 可能需要将一些信息发送到前端
                return redirect(f'{settings.FRONT_END_URL}/login?token={access_token}')
            # 认证失败的处理
            return redirect(f'{settings.FRONT_END_URL}/login?error=oauth2_failure')
        except AuthException as e:
            # 处理可能的认证异常
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


class UserInfo(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def get_user_info(self, request):
        if request.user.is_authenticated:
            return JsonResponse(
                {"username": request.user.username, "role": request.user.role, "email": request.user.email})
        else:
            return JsonResponse({"error": "Not authenticated"}, status=401)
