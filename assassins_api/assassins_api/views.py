from assassins_api.models import Game
from assassins_api.models import Player
from assassins_api.serializers import GameSerializer
from assassins_api.serializers import PlayerSerializer
from assassins_api.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
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
    
def get_player(pk):
  try:
    return Player.objects.get(pk=pk)
  except Player.DoesNotExist:
    raise Http404

def players_within_range(player1, player2):
  return True

class User_Create(APIView):
  permission_classes = (AllowAny,)
  def post(self,request):
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
      User.objects.create_user(
          serialized.init_data['username'],
          serialized.init_data['email'],
          serialized.init_data['password']
      )
      return Response(status=status.HTTP_201_CREATED)
    else:
      return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    
class Game_Create(APIView):
  def post(self, request):
    serializer = GameSerializer(data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Game_Status(APIView):
  def get(self, request, pk):
    game = get_game(pk)
    serializer = GameSerializer(game)
    return Response(game.data)
    
  def delete(self, request, pk):
    game = get_game(pk)
    game.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
class Player_Status(APIView):
  def get(self, request, pk):
    player = get_player(pk)
    serializer = PlayerSerializer(game)
    return Response(player.data)
    
  def post(self, request, pk):
    serializer = PlayerSerilizer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  def delete(self, request, pk):
    player = get_player(pk)
    player.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
class Game_Start(APIView):
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
    
class Player_Attack(APIView):
  def post(self, request, pk):
    player = get_player(pk)
    target = get_player(player.target_id)
    if(players_within_range(player, target)):
      target.alive = False
      player.target = target.target
      return Response(data="Kill", status=HTTP_200_OK)
    return Response(data="Target not in range", status=HTTP_BAD_REQUEST)