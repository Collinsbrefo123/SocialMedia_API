from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .serializers import RoomSerializer, MessageSerializer
from .models import Room, Message
from rest_framework.response import Response


# Create your views here.

class RoomAPIView(GenericAPIView):
    serializer_class = RoomSerializer

    def post(self, request):
        data = request.data
        room = data.get('room_name', '')
        print(room)
        if Room.objects.filter(room_name=room).exists():
            room_now = Room.objects.get(room_name=room)
            serializer = RoomSerializer(room_now)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = RoomSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class MessageAPIView(GenericAPIView):
    serializer_class = MessageSerializer

    def get(self, request):
        messages = Message.objects.all()
        serializers = MessageSerializer(messages, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
