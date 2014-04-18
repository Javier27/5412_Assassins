from assassins_api.serializers import ProfileSerializer
from assassins_api.serializers import FriendSerializer
from assassins_api.models import Profile
from assassins_api.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

def get_profile(pk):
  try:
    return Profile.objects.get(pk=pk)
  except Profile.DoesNotExist:
    raise Http404

class Create(APIView):
  permission_classes = (AllowAny,)
  def post(self,request):
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
      user = User.objects.create_user(
          serialized.init_data['username'],
          serialized.init_data['email'],
          serialized.init_data['password']
      )
      profile = Profile(user=user,email=user.email,username=user.username)
      profile.save()
      return Response(status=status.HTTP_201_CREATED)
    else:
      return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

#TODO: Password reset feature

class Delete(APIView):
  def delete(self, request):
    profile = get_profile(request.DATA.get('id'))
    profile.delete()
    return Response(status=status.HTTP_NO_CONTENT)

#TODO try catch?      
class Friend(APIView):
  # add a friend for profile with given pk
  def post(self, request):
    profile = get_profile(request.DATA.get('id'))
    profile.friends.add(request.DATA.get('friend_id'))
    profile.save()
    return Response(status=status.HTTP_200_OK)
 
class Friends_List(APIView):
  def get(self, request, pk):
    profile = get_profile(pk)
    serializer = FriendSerializer(profile.friends.all())
    return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class Unfriend(APIView):
  def delete(self,request):
    profile = get_profile(request.DATA.get('id'))
    profile.friends.remove(request.DATA.get('friend'))
    return Response(status=status.HTTP_204_NO_CONTENT)