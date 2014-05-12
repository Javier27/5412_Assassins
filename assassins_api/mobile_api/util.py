from django.http import HttpResponse
from django.template import Context, loader
from mobile_api import models
from mobile_api.models import Game
from mobile_api.models import Player
from django.db.models import Q
import math

  
all = 0
pending = 1
active = 2
ended = 3
owned = 4

def get_profile_given_user_id(user_id):
  profile = models.Profile.objects.filter(user=user_id).get();
  return profile;
  
def get_games_for_profile(profile, status=all):
  games =[]
  if status is owned:
    games = Game.objects.filter(owner=profile)
  else:
    players = profile.players.all()
    for player in players:
      if status is all:
        games.append(player.game)
      elif int(player.game.game_status) == int(status):
        games.append(player.game)
  return games
  
def get_players_for_profile(profile, status=all):
  games =[]
  players = profile.players.all()
  for player in players:
    if status is all:
      games.append(player)
    elif int(player.game.game_status) == int(status):
      games.append(player)
  return games

def get_player_given_profile_game(user_id, game_id):
  return Player.objects.filter(Q(profile=user_id)&Q(game=game_id))[0]
  
  
def get_game(pk):
  try:
    return Game.objects.get(pk=pk)
  except Game.DoesNotExist:
    raise Http404
    
def distance_between_two_points(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)
  
def user_close_enough(x1, y1, x2, y2):
  dis = distance_between_two_points(x1,y1,x2,y2)
  return dis < 40.0
  
def time_close_enough(t1):
  return True
  