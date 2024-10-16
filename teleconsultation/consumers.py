import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TeleconsultationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.teleconsultation_id = self.scope['url_route']['kwargs']['teleconsultation_id']
        self.room_group_name = f'teleconsultation_{self.teleconsultation_id}'

        # Join the room group for signaling and chat
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        if message_type == 'signal':
            signal = data['signal']
            await self.channel_layer.group_send(
                self.room_group_name, 
                {'type': 'send_signal', 'signal': signal}
            )
        elif message_type == 'chat':
            message = data['message']
            await self.channel_layer.group_send(
                self.room_group_name, 
                {'type': 'send_chat', 'message': message}
            )

    # Send signaling data to WebSocket
    async def send_signal(self, event):
        signal = event['signal']
        await self.send(text_data=json.dumps({'type': 'signal', 'signal': signal}))

    # Send chat messages to WebSocket
    async def send_chat(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'type': 'chat', 'message': message}))
