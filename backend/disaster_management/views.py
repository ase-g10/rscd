import requests
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import action

from django.http import JsonResponse
import json

from django.conf import settings


class DisasterView(viewsets.ViewSet):
    @action(detail=False, methods=['post', 'get'])
    def post_location(self, request, pk=None):
        try:
            data = request.data

            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude is None:
                return JsonResponse({"status": "error", "message": "Latitude cannot be empty."}, status=400)
            if longitude is None:
                return JsonResponse({"status": "error", "message": "Longitude cannot be empty."}, status=400)

            print(latitude)
            print(longitude)
            # 在这里处理数据（例如，保
            # 返回成功响应
            return JsonResponse({"status": "success", "message": "Location received successfully."})
        except json.JSONDecodeError:
            # 如果请求的内容不是有效的 JSON，返回错误响应
            return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)
        except Exception as e:
            # 处理其他意外错误
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

