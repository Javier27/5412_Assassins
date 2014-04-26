from assassins_api.serializers import ProfileSerializer
from assassins_api.serializers import FriendSerializer
from assassins_api.models import Profile
from assassins_api.controllers import profile_controller
from assassins_api.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from assassins_api import util
from rest_framework.authentication import SessionAuthentication

class List_Games(APIView):
  authentication_classes = (SessionAuthentication,)
  def get(self,request):
    profile = profile_controller.get_profile(request.user.id)
    return util.return_html("index.html",{'games':profile.owned_games.all()})
  
