from assassins_api.serializers import ProfileSerializer
from assassins_api.serializers import FriendSerializer
from assassins_api.models import Profile
from assassins_api.serializers import UserSerializer
from assassins_api import util
from django.http import Http404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.template import Context, loader 
from django.shortcuts import redirect
from django.db.models import Q

def get_profile(pk):
  try:
    return Profile.objects.get(pk=pk)
  except Profile.DoesNotExist:
    raise Http404

class Create(APIView):
  permission_classes = (AllowAny,)
  def get(self,request):
    # Load the template myblog/templates/index.html
    template = loader.get_template('user_register.html')
 
    # Context is a normal Python dictionary whose keys can be accessed in the template index.html
    return util.return_html('user_register.html', {})
  
  def post(self,request):
    serialized = UserSerializer(data=request.DATA)
    if request.DATA.get('password') != request.DATA.get('confirm_password'):
      if request.DATA.get("admin_panel"):
        return util.return_html("user_register.html",{'confirm_password_error':'Passwords do not match'})
      else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    else:       
      if serialized.is_valid():
        user = User.objects.create_user(
            serialized.init_data['username'],
            serialized.init_data['email'],
            serialized.init_data['password']
        )
        profile = Profile(user=user,email=user.email,username=user.username)
        profile.save()
      
        if request.DATA.get('admin_panel'):
          return redirect('/admin_panel/');
        else:
          return Response(status=status.HTTP_201_CREATED)
      else:
        if request.DATA.get("admin_panel"):
          return util.return_html("user_register.html",serialized.errors)
        else:
          return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
          
class Self_Status(APIView):
  def get(self, request):
    profile = ProfileSerializer(util.get_profile_given_user_id(request.user.id))
    return Response(profile.data, status=status.HTTP_200_OK)
    
    
class Status(APIView):
  def get(self, request, pk):
    profile = ProfileSerializer(get_profile(pk))
    return Response(profile.data,status=status.HTTP_200_OK)
    
class Find(APIView):
  def get(self, request):
    search = request.GET.get('search')
    print search
    profile = Profile.objects.filter(Q(username__contains=search) | Q(email__contains=search))
    result = ProfileSerializer(profile.all())
    return Response(result.data, status=status.HTTP_200_OK)

#TODO: Password reset feature

class Delete(APIView):
  def delete(self, request):
    profile = util.get_profile_given_user_id(request.user.id)
    profile.delete()
    return Response(status=status.HTTP_NO_CONTENT)
    
class Upload_Picture(APIView):
  def post(self,request):
    profile = get_profile(request.DATA.get('id'))
    picture = request.DATA.get('picture')
    profile.picture = picture
    profile.save()
    return Response("Ok",status=status.HTTP_200_OK)

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