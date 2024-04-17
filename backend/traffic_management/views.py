import random
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from models.models import DrivingLocation, User
from apscheduler.schedulers.background import BackgroundScheduler
from rest_framework.permissions import IsAuthenticated
import logging
import joblib

from tensorflow.keras.models import load_model
import numpy as np

from .CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication


# logger = logging.getLogger(__name__)


# def disable_old_locations():
#     print("Running disable_old_locations task")
#     time_threshold = timezone.now() - timedelta(seconds=40)
#     old_locations = DrivingLocation.objects.filter(update_time__lt=time_threshold)
#     old_locations.update(is_disabled=True)
#     print("Disabled {} old locations".format(len(old_locations)))
#
#
# def delete_disabled_locations():
#     print("Running delete_disabled_locations task")
#     disabled_locations = DrivingLocation.objects.filter(is_disabled=True)
#     count = disabled_locations.count()
#     disabled_locations.delete()
#     print("Deleted {} disabled locations".format(count))


def shift_table(driving_location):
    driving_location.lat1, driving_location.lon1, driving_location.time1 = driving_location.lat2, driving_location.lon2, driving_location.time2
    driving_location.lat2, driving_location.lon2, driving_location.time2 = driving_location.lat3, driving_location.lon3, driving_location.time3
    driving_location.lat3, driving_location.lon3, driving_location.time3 = driving_location.lat4, driving_location.lon4, driving_location.time4
    driving_location.lat4, driving_location.lon4, driving_location.time4 = driving_location.lat5, driving_location.lon5, driving_location.time5
    driving_location.lat5, driving_location.lon5, driving_location.time5 = driving_location.lat6, driving_location.lon6, driving_location.time6
    driving_location.lat6, driving_location.lon6, driving_location.time6 = driving_location.lat7, driving_location.lon7, driving_location.time7
    driving_location.lat7, driving_location.lon7, driving_location.time7 = driving_location.lat8, driving_location.lon8, driving_location.time8
    driving_location.lat8, driving_location.lon8, driving_location.time8 = driving_location.lat9, driving_location.lon9, driving_location.time9
    driving_location.lat9, driving_location.lon9, driving_location.time9 = driving_location.lat10, driving_location.lon10, driving_location.time10


def call_model(input):

    # Load model and make predictions
    model = load_model('LSTM_Vehicle_Location_Prediction.h5')
    prediction = model.predict(input)

    return prediction

def convert_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


import numpy as np
import joblib
from django.utils import timezone

def convert_to_seconds(t):
    h, m, s = map(int, t.split(':'))
    return h * 3600 + m * 60 + s

def call_model(input_data):
    # Dummy function to represent model prediction
    return np.random.random(), np.random.random()

def predict_location(loc):
    # Load the scaler objects
    latitude_scaler = joblib.load('traffic_management/scaler/latitude_scaler.gz')
    longitude_scaler = joblib.load('traffic_management/scaler/longitude_scaler.gz')
    time_scaler = joblib.load('traffic_management/scaler/time_scaler.gz')

    # Create a sequence of the last 10 locations and times
    lats = [loc.lat1, loc.lat2, loc.lat3, loc.lat4, loc.lat5, loc.lat6, loc.lat7, loc.lat8, loc.lat9, loc.lat10]
    lons = [loc.lon1, loc.lon2, loc.lon3, loc.lon4, loc.lon5, loc.lon6, loc.lon7, loc.lon8, loc.lon9, loc.lon10]
    times = [loc.time1, loc.time2, loc.time3, loc.time4, loc.time5, loc.time6, loc.time7, loc.time8, loc.time9, loc.time10]
    times = [t.strftime("%H:%M:%S") for t in times]
    times_in_seconds = [convert_to_seconds(t) for t in times]

    # Normalize the sequence one by one
    lats_normalized = np.array([latitude_scaler.transform([[lat]])[0][0] for lat in lats])
    lons_normalized = np.array([longitude_scaler.transform([[lon]])[0][0] for lon in lons])
    times_normalized = np.array([time_scaler.transform([[t]])[0][0] for t in times_in_seconds])

    current_time = timezone.now().strftime("%H:%M:%S")
    current_time_in_seconds = convert_to_seconds(current_time)
    current_time_normalized = time_scaler.transform([[current_time_in_seconds]])[0][0]

    # Reshape the input data to match the input shape of the model
    input_data = np.column_stack((times_normalized, lats_normalized, lons_normalized))
    input_data = np.expand_dims(input_data, axis=0)

    print(f'Input data: {input_data}')

    # Call the model with the normalized data
    predicted_lat, predicted_lon = call_model(input_data)

    print(f'Predicted lat: {predicted_lat}, lon: {predicted_lon}')

    # Inverse transform the predicted values
    predicted_lat = latitude_scaler.inverse_transform([[predicted_lat]])[0][0]
    predicted_lon = longitude_scaler.inverse_transform([[predicted_lon]])[0][0]

    print(f'Predicted lat: {predicted_lat}, lon: {predicted_lon}')

    return predicted_lat, predicted_lon


class TrafficView(viewsets.ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @action(detail=False, methods=['get'])
    def get_driving_location(self, request):
        all_locations = DrivingLocation.objects.all()

        time_threshold_predict = timezone.now() - timedelta(seconds=30)
        time_threshold_drop = timezone.now() - timedelta(seconds=600)

        locations_list = []
        for loc in all_locations:
            if loc.time10 < time_threshold_drop:
                loc.delete()
                continue

            elif loc.time10 < time_threshold_predict and loc.time1 is not None:
                shift_table(loc)

                predicted_lat, predicted_lon = predict_location(loc)

                loc.lat10, loc.lon10 = predicted_lat, predicted_lon

                locations_list.append({
                    'latitude': predicted_lat,
                    'longitude': predicted_lon,
                    'user_role': loc.user.role
                })
            else:
                locations_list.append({
                    'latitude': loc.lat10,
                    'longitude': loc.lon10,
                    'user_role': loc.user.role
                })

        print(f'Locations: {locations_list}')

        return JsonResponse({"status": "success", "locations": locations_list})


    @action(detail=False, methods=['post'])
    def save_driving_location(self, request):
        print("Start save_driving_location")
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User not authenticated."})

        user = request.user
        print("User: {}".format(user))

        if not user:
            return JsonResponse({"status": "error", "message": "User not found."})

        lat = request.data.get('latitude')
        lon = request.data.get('longitude')

        print("Latitude: {}".format(lat))
        print("Longitude: {}".format(lon))

        if not lat or not lon:
            return JsonResponse({"status": "error", "message": "Latitude and longitude are required."})

        try:
            driving_location = DrivingLocation.objects.get(user=user)
            print("Updating driving location entry for user {}".format(user.username))
            shift_table(driving_location)

            driving_location.lat10 = lat
            driving_location.lon10 = lon
            driving_location.time10 = timezone.now()

        except DrivingLocation.DoesNotExist:
            print("Creating new driving location entry for user {}".format(user.username))
            DrivingLocation.objects.create(user=user)
            driving_location = DrivingLocation.objects.get(user=user)

            driving_location.lat10 = lat
            driving_location.lon10 = lon
            driving_location.time10 = timezone.now()

        driving_location.save()

        return JsonResponse({"status": "success", "message": "Location saved successfully."})

    @action(detail=False, methods=['post'])
    def test_fake_data(self,request):
        def create_driving_location(user_id):
            User = get_user_model()

            # Get the user with the given ID
            user = User.objects.get(id=user_id)

            # Generate random latitude and longitude near Trinity College Dublin
            lat = random.uniform(53.3438 - 0.01, 53.3438 + 0.01)
            lon = random.uniform(-6.2546 - 0.01, -6.2546 + 0.01)

            # Use the current time
            time = timezone.now()

            # Create a new DrivingLocation object
            driving_location = DrivingLocation.objects.create(
                user=user,
                lat10=lat,
                lon10=lon,
                time10=time,
            )

            return driving_location
        user_ids = User.objects.values_list('id', flat=True)
        for user_id in user_ids:
            create_driving_location(user_id)
        return JsonResponse({"status": "success", "message": "Fake data created successfully."})
