import requests
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from django.core import serializers
from django.http import JsonResponse
import json
from models.models import Disaster
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

    @action(detail=False, methods=['post', 'get'])
    def disaster_view(self, request):
        try:
            disaster_queryset = Disaster.objects.all()
            disaster_queryset = Disaster.objects.filter(name='testDisaster')
            print(disaster_queryset)
            disaster_serialized = serializers.serialize('json', disaster_queryset)
            # Sending serialized data as a response
            return JsonResponse({"message": json.loads(disaster_serialized)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

class DisasterModify(viewsets.ViewSet):
    @action(detail=False, methods=['post', 'get'])
    def write(self, request):
        try:
            data = request.data
            name = data.get('name')
            description = data.get('description')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            location = data.get('location')
            radius = data.get('radius')
            type = data.get('type')
            disaster = Disaster()
            disaster.name = name
            disaster.description = description
            disaster.latitude = latitude
            disaster.longitude = longitude
            disaster.location = location
            disaster.radius = float(radius)
            disaster.type = type
            disaster.save()
            return JsonResponse({"message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
