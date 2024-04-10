# your_app_name/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from models.models import Disaster  # 假设你的模型名称为Disaster
from .consumers import DisasterAlertConsumer  # 假设你已经创建了一个WebSocket消费者处理预警通知

@receiver(post_save, sender=Disaster)
def send_alert(sender, instance, created, **kwargs):
    if created:
        # 这里我们假设有一个函数来处理实际的消息发送
        DisasterAlertConsumer.send_alert_message({
            'type': 'disaster.alert',
            'message': f'New disaster alert: {instance.description}'  # 假设instance有一个描述字段
        })
