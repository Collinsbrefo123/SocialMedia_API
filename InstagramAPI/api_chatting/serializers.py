from rest_framework import serializers, fields
from .models import Room, Message


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_name']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['value', 'user', 'room', 'date']
