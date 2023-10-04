# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VacancyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Подключаемся к группе уведомлений
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы уведомлений
        await self.channel_layer.group_discard("notifications", self.channel_name)

    # Обрабатываем получение сообщения и отправляем его обратно клиенту
    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
