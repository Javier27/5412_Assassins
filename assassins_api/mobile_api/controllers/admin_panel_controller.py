from mobile_api.serializers import ProfileSerializer
from mobile_api.serializers import FriendSerializer
from mobile_api.models import Profile
from mobile_api.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from mobile_api import util

class List_Games(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def get(self, request):
    return util.return_html("user_register.html",[])