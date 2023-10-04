import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Добавляем пользователя в группу 'chat_room'
        self.room_group_name = 'chat_room'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Удаляем пользователя из группы 'chat_room'
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Отправляем сообщение всем участникам группы
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Этот метод будет вызываться, когда сообщение отправляется участникам группы
    async def chat_message(self, event):
        message = event['message']

        # Отправляем сообщение обратно клиенту
        await self.send(text_data=json.dumps({
            'message': message
        }))
        

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))



async def receive(self, text_data):
    try:
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', None)
        if not message:
            return

        await self.send(text_data=json.dumps({
            'message': message
        }))
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON")


