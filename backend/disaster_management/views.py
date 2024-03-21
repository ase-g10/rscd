from math import sin, cos, atan2, radians, pi, sqrt

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
            name = data.get('name')
            description = data.get('description')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            location = data.get('location')
            radius = data.get('radius')
            type = data.get('type')
            contact = data.get('contact')
            imageUrl = "" if data.get('imageUrl') == None else data.get('imageUrl')
            disaster = Disaster()
            disaster.name = name
            disaster.description = description
            disaster.latitude = latitude
            disaster.longitude = longitude
            disaster.location = location
            disaster.radius = float(radius)
            disaster.type = type
            disaster.image_url = imageUrl
            disaster.contact = contact
            disaster.save()

            if latitude is None:
                return JsonResponse({"status": "error", "message": "Latitude cannot be empty."}, status=400)
            if longitude is None:
                return JsonResponse({"status": "error", "message": "Longitude cannot be empty."}, status=400)
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
    def read_all_verified(self, request):
        try:
            # disaster_queryset = Disaster.objects.all()
            disaster_queryset = Disaster.objects.filter(verified_status="1")
            disaster_serialized = serializers.serialize('json', disaster_queryset)
            # Sending serialized data as a response
            return JsonResponse({"message": json.loads(disaster_serialized)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    @action(detail=False, methods=['post', 'get'])
    def read_all_verifying(self, request):
        try:
            # disaster_queryset = Disaster.objects.all()
            disaster_queryset = Disaster.objects.all(verified_status="0")
            disaster_serialized = serializers.serialize('json', disaster_queryset)
            # Sending serialized data as a response
            return JsonResponse({"message": json.loads(disaster_serialized)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    @action(detail=False, methods=['post'])
    def calculate_safePoint(self, request):
        data = request.data
        print(data)
        user_latitude = float(data.get('latitude'))

        user_longitude = float(data.get('longitude'))
        print(user_latitude, user_longitude)
        if user_latitude is None:
            return JsonResponse({"status": "error", "message": "Latitude cannot be empty."}, status=400)
        if user_longitude is None:
            return JsonResponse({"status": "error", "message": "Longitude cannot be empty."}, status=400)
        def calculate_bearing(lat1, lng1, lat2, lng2):
            """
            计算从点1到点2的方位角（以北为0度，顺时针方向）
            """
            lat2 = float(lat2)
            lng2 = float(lng2)
            lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
            d_lng = lng2 - lng1
            y = sin(d_lng) * cos(lat2)
            x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(d_lng)
            bearing = atan2(y, x)
            bearing = (bearing + 2 * pi) % (2 * pi)  # 规范化为0到2π之间
            return bearing

        def haversine(lon1, lat1, lon2, lat2):
            """
            计算两个经纬度点之间的距离（单位：米）
            """
            lon1 = float(lon1)
            lat1 = float(lat1)
            lon2 = float(lon2)
            lat2 = float(lat2)
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            r = 6371000  # 地球平均半径，单位为米
            return c * r

        def is_user_in_disaster_area(user_lat, user_lng):
            for disaster in Disaster.objects.all():
                distance = haversine(user_lng, user_lat, disaster.longitude, disaster.latitude)
                if distance <= disaster.radius:
                    # 用户在灾难影响范围内
                    return True, disaster
            return False, None

        def calculate_escape_point(user_lat, user_lng, disaster):
            user_lat, user_lng = float(user_lat), float(user_lng)
            disaster_lat, disaster_lng, disaster_radius = map(float,
                                                              [disaster.latitude, disaster.longitude, disaster.radius])

            bearing = calculate_bearing(user_lat, user_lng, disaster_lat, disaster_lng)
            print(bearing)
            safe_lat = disaster_lat + (disaster_radius / 6371000) * cos(bearing) * (180 / pi)
            safe_lng = disaster_lng + (disaster_radius / 6371000) * sin(bearing) * (180 / pi) / cos(
                radians(disaster_lat))

            return safe_lat, safe_lng

        # 检查用户是否处于任何灾难的影响范围内
        # user_lat, user_lng = 40.7128, -74.0060  # 假设的用户位置
        in_disaster_area, disaster = is_user_in_disaster_area(user_latitude, user_longitude)
        print(in_disaster_area, disaster)
        if in_disaster_area:
            safe_lat, safe_lng = calculate_escape_point(user_latitude, user_longitude, disaster)
            print(f"用户在灾难范围内，最近安全点的坐标：{safe_lat}, {safe_lng}")
            return JsonResponse({'safe_lat': safe_lat, 'safe_lng': safe_lng})
        else:
            print("用户不在任何灾难的影响范围内。")
            return JsonResponse({"status": "error", "message": "User is not in any disaster's impact area."})


class DisasterModify(viewsets.ViewSet):
    @action(detail=False, methods=['post', 'get'])
    def write(self, request):
        try:
            data = request.data
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            verified_status = data.get('verified_status')
            Tmp = Disaster.objects.filter(latitude=latitude, longitude=longitude)
            for tmp in Tmp:
                tmp.verified_status = verified_status
                tmp.save()
            return JsonResponse({"message": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
