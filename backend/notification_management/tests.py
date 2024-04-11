# # notification_management/tests.py
# from channels.testing import ChannelsLiveServerTestCase
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# import websockets
# import json
#
#
# class NotificationTests(ChannelsLiveServerTestCase):
#     def test_alert_message(self):
#         async def connect_and_send_alert():
#             # Connect to the WebSocket server
#             async with websockets.connect("ws://127.0.0.1:8000/ws/notifications/") as websocket:
#                 # Now trigger the view logic that sends the message (you might need to call the view directly or perform an HTTP request)
#                 # For demonstration, we're calling a hypothetical function that triggers the alert
#                 send_alert_via_view()
#
#                 # Wait for a message from the WebSocket
#                 response = await websocket.recv()
#                 response_data = json.loads(response)
#                 self.assertEqual(response_data['message'], 'Alert message here')
#
#         # Run the async connect and test logic
#         self.loop.run_until_complete(connect_and_send_alert())
#
#
# def send_alert_via_view():
#     # This function should mimic the logic in your view that triggers the WebSocket message.
#     # For this example, we are manually triggering the group send.
#     # In a real test, you might use Django's test client to make an HTTP request to the view.
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "alert_group",
#         {
#             "type": "send_alert",
#             "message": "Alert message here",
#         }
#     )