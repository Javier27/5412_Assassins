from assassins_api.models import Game
from assassins_api.serializers import GameSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.contrib.auth.models import User

#TODO: Stuff at top should probably be moved into another file
GAME_STATUS =[(1,'pending'),(2,'in_progress'),(3,'over')]

def get_game(pk):
  try:
    return Game.objects.get(pk=pk)
  except Game.DoesNotExist:
    raise Http404
    
class Create(APIView):
  def post(self, request):
    data = request.DATA
    data.__setitem__('owner', request.user.id)
    data.__setitem__('status',0)
    serializer = GameSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class List_All_Playing(APIView):
  def get(self, request):
    profile = util.get_profile_given_user_id(request.user.user_id)
    games = util.get_games_for_profile(profile)
    serializer = GameSerializer(games)
    return Response(serializer.data)
  
    
class Status(APIView):
  def get(self, request, pk):
    game = get_game(pk)
    serializer = GameSerializer(game)
    return Response(game.data, status=status.HTTP_200_OK)
    
  #TODO make sure owner
  def delete(self, request, pk):
    game = get_game(pk)
    game.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

#TODO make sure owner
class Start(APIView):
  def post(self, request, pk):
    game = get_game(pk)
    if (int(game.status) != 1):
      return Response(data="Game has already started", status=status.HTTP_400_BAD_REQUEST)
    players = Player.objects.filter(game_id=pk)
    player_ids = list(Player.objects.values_list('id',flat=True).filter(game_id=pk))
    random.shuffle(player_ids)
    #Assign a player their target by id aslong as its not themselfs
    for player in players:
      for p_id in player_ids:
        if p_id != player.id:
          player.target = Player(id=p_id)
          player_ids.remove(p_id)
          player.save()
          break
    game.status=2
    game.save()
    return Response(status=status.HTTP_200_OK)