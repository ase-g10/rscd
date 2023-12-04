import requests
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from social_core.exceptions import AuthException

from django.http import JsonResponse
import json

from django.conf import settings


class DisasterView(viewsets.ViewSet):
    @action(detail=False, methods=['post', 'get'])
    def post_location(self, request, pk=None):
        try:
            # 将请求的 JSON 转换成 Python 字典
            data = request.data

            # 提取纬度和经度数据
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            # 在这里处理数据（例如，保
            # 返回成功响应
            return JsonResponse({"status": "success", "message": "Location received successfully."})
        except json.JSONDecodeError:
            # 如果请求的内容不是有效的 JSON，返回错误响应
            return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)
        except Exception as e:
            # 处理其他意外错误
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
