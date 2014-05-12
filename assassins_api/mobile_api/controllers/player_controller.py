from mobile_api.models import Player
from mobile_api.serializers import PlayerSerializer
from mobile_api.serializers import AssassinationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from mobile_api import util

def get_player(pk):
  try:
    return Player.objects.get(pk=pk)
  except Player.DoesNotExist:
    raise Http404


class Status(APIView):
  def get(self, request, pk):
    profile = util.get_profile_given_user_id(request.user.id)
    players = Player.objects.filter(profile=profile.id).filter(game=pk)
    if len(players) < 1:
      return Response("No Such Player", status=status.HTTP_400_BAD_REQUEST)
    serializer = PlayerSerializer(players[0])
    return Response(serializer.data,status=status.HTTP_200_OK)
    
  def delete(self, request, pk):
    player = get_player(pk)
    player.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
class Create_Multiple(APIView):
  def post(self, request):
    players = request.POST.get('players')
    players = players.replace(',', '&')
    players = players.split(";")
    response = ""
    for player in players:
      print player
      qdict = QueryDict(player)
      serializer = PlayerSerializer(data=qdict)
      print serializer.data
      if serializer.is_valid():
        serializer.save()
        response = response + " " + str(serializer.data)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(response, status=status.HTTP_201_CREATED)

class Create(APIView):
  def post(self, request):
    serializer = PlayerSerializer(data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Attack(APIView):
  def post(self, request):
    serializer = AssassinationSerializer(data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(data="Pending", status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)