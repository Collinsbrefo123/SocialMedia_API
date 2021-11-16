from django.urls import path
from api_chatting import views
urlpatterns = [
    path('home/', views.RoomAPIView.as_view(), name="home"),
    path('room/', views.MessageAPIView.as_view(), name="room"),
]