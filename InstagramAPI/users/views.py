import json

import datetime
import jwt
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Feeds
from .serializers import UserSerializer, FeedSerializer


# Create your views here.

class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']
#
#         user = User.objects.filter(email=email).first()
#
#         if user is None:
#             raise AuthenticationFailed('User not found')
#
#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password ')
#
#         payload = {
#             "id": user.id,
#             "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.now()
#         }
#         token = jwt.encode(payload, 'secret', algorithm='HS256')
#
#         user_serializer = UserSerializer(user)
#         print(user_serializer.data['id'])
#
#         response = Response()
#         response.set_cookie(key='jwt', value=token,httponly=True,)
#         response.data = {
#             'jwt': token
#             # 'user_details': user_serializer.data,
#             # 'email': user_serializer.data['email'],
#             # 'username': user_serializer.data['username']
#         }
#
#         return response
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        user_serializer = UserSerializer(user)

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt_instagram', value=token, httponly=True)
        response.data = {
            'jwt_instagram': token,
            # 'user_details': user_serializer.data,
        }
        return response


class UserAPIView(APIView):
    def get(self, request):
        token = request.COOKIES['jwt_instagram']
        print('token ', token)
        if not token:
            raise AuthenticationFailed("Please one")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("User unauthenticated. Wrong User Details")

        user = User.objects.get(id=payload['id'])
        print(payload)
        user_serializer = UserSerializer(user)
        print(user_serializer.data)

        feeds = Feeds.objects.filter(user=payload['id'])
        for feed in feeds:
            print(feed.imgFeed.url)
        feeds_serializer = FeedSerializer(feeds, many=True)
        print(feeds_serializer.data)

        return Response({"user_details": user_serializer.data, "feeds": feeds_serializer.data}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt_instagram')
        response.data = {
            "status": status.HTTP_200_OK
        }
        return response


class CreateFeedAPIView(APIView):
    def post(self, request, format=None):
        token = request.COOKIES['jwt_instagram']
        print('token ', token)
        if not token:
            raise AuthenticationFailed("Please one")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("User unauthenticated. Wrong User Details")
        # title = request.data['title']
        # caption = request.data['caption']
        imgFeed = request.data.get('imgFeed')
        email = json.loads(request.data.get('email'))
        print('awesome')
        print(request.data)
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(imgFeed=imgFeed, user=User.objects.filter(email=email).first())
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

        # if serializer.is_valid():
        #     serializer.save(user=User.objects.filter(email=email).first())
        #     return Response(serializer.data,status=status.HTTP_200_OK)
        # return Response({'error':'error with file'}, status=status.HTTP_400_BAD_REQUEST)
        # serializer = FeedSerializer(data=request.data)
        # if serializer.is_valid():
        #     form = serializer.save(commit=False)
        #     form.user = User.objects.filter(email=email)
        #     form.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(status=status.HTTP_400_BAD_REQUEST)
