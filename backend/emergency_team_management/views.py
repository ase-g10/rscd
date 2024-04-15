import json

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from models.models import Disaster, Log
from django.http import JsonResponse
from django.core import serializers
# Create your views here.
class EmergencyView(viewsets.ViewSet):
    @action(detail=False, methods=['post', 'get'])
    def response(self, request):
        try:
            data = request.data
            disaster_name = data.get('name')
            description = data.get('description')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            location = data.get('location')
            responsible_team = data.get('username')
            Tmp = Disaster.objects.filter(latitude=latitude, longitude=longitude)
            for tmp in Tmp:
                is_onging = tmp.is_onging
                if not is_onging:
                    return JsonResponse({"status": "error", "message": "already deleted this disaster"})
                else:
                    # terminate the disaster
                    tmp.is_onging = False
                    tmp.save()
                type = tmp.type
                radius = tmp.radius
                create_time = tmp.create_time
            log = Log()
            log.disaster_name = disaster_name
            log.description = description
            log.latitude = latitude
            log.longitude = longitude
            log.location = location
            log.responsible_team = responsible_team
            log.radius = float(radius)
            log.type = str(type)
            log.create_time = create_time
            log.save()
            return JsonResponse({"message": "Successful!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    @action(detail=False, methods=['post', 'get'])
    def read_all_logs(self, request):
        try:
            Tmp = Log.objects.all()
            new_Tmp = serializers.serialize('json', Tmp)
            return JsonResponse({"message": json.loads(new_Tmp)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    @action(detail=False, methods=['post', 'get'])
    def read_specific_log(self, request):
        try:
            data = request.data
            disaster_name = data.get('disaster_name')
            Tmp = Log.objects.filter(disaster_name=disaster_name)
            new_Tmp = serializers.serialize('json', Tmp)
            return JsonResponse({"message": json.loads(new_Tmp)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)