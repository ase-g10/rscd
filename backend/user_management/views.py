import requests
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from social_core.exceptions import AuthException
from django.http import JsonResponse
import json
from django.conf import settings
from models.models import User
class Login(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def log_in(self, request, pk=None):
        try:
            data = request.data

            email = data.get('email')
            pwd = data.get('password')

            # Todo 邮箱是否存在，email验证，pwd验证是否相同，密码加密，存数据库，
            if email is "":
                return JsonResponse({"status": "error", "message": "email cannot be empty."}, status=400)
            if pwd is "":
                return JsonResponse({"status": "error", "message": "password cannot be empty."}, status=400)

            print(email)
            print(pwd)

            return JsonResponse({"status": "success", "message": "Account login successfully."})
        except json.JSONDecodeError:

            return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)
        except Exception as e:

            return JsonResponse({"status": "error", "message": str(e)}, status=500)


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
