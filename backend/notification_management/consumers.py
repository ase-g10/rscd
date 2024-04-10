# your_app_name/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class DisasterAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 将新连接的用户加入到特定的群组，以便可以向所有用户广播消息
        await self.channel_layer.group_add(
            "disaster_alerts",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # 用户断开连接时，将其从群组中移除
        await self.channel_layer.group_discard(
            "disaster_alerts",
            self.channel_name
        )

    # 用于接收来自Django信号的消息并广播给所有连接的WebSocket客户端
    @classmethod
    def send_alert_message(cls, message):
        # 注意，这里使用的是async_to_sync()，因为信号处理器默认不是异步的
        async_to_sync(cls.channel_layer.group_send)(
            "disaster_alerts",
            {
                'type': 'disaster_alert',
                'message': message
            }
        )

    # 客户端将收到的消息类型为disaster_alert的处理
    async def disaster_alert(self, event):
        message = event['message']

        # 发送消息到WebSocket客户端
        await self.send(text_data=json.dumps({
            'message': message
        }))
