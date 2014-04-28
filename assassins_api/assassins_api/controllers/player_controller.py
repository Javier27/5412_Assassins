from assassins_api.models import Player
from assassins_api.serializers import PlayerSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def get_player(pk):
  try:
    return Player.objects.get(pk=pk)
  except Player.DoesNotExist:
    raise Http404

def players_within_range(player1, player2):
  return True  

class Status(APIView):
  def get(self, request, pk):
    player = get_player(pk)
    serializer = PlayerSerializer(game)
    return Response(player.data)
    
  def delete(self, request, pk):
    player = get_player(pk)
    player.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class Create(APIView):
  def post(self, request):
    serializer = PlayerSerilizer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
class Attack(APIView):
  def post(self, request, pk):
    player = get_player(pk)
    target = get_player(player.target_id)
    if(players_within_range(player, target)):
      target.alive = False
      player.target = target.target
      return Response(data="Kill", status=HTTP_200_OK)
    return Response(data="Target not in range", status=HTTP_400_BAD_REQUEST)