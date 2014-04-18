from rest_framework import serializers
from assassins_api.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id','username','email')
    
class GameSerializer(serializers.ModelSerializer):
  players = serializers.PrimaryKeyRelatedField(many=True)
  class Meta:
    model = Game
    fields = ('name', 'owner', 'status')
    
class PlayerSerializer(serializers.ModelSerializer):
  target = serializers.PrimaryKeyRelatedField(many=False)
  class Meta:
    model = Player
    fields = ('alive','game','target','user')
    
class PowerUpSerializer(serializers.ModelSerializer):
  class Meta:
    model = PowerUp
    fields = ('name','spawn_chance')
    
class InventorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Inventory
    fields = ('player','item')

class ProfileSerializer(serializers.ModelSerializer):
  players = serializers.PrimaryKeyRelatedField(many=True)
  games = serializers.PrimaryKeyRelatedField(many=True)
  class Meta:
    model = Profile
    fields = ('friends','players','owned_games','user','username','email')

class FriendSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('username','email','id')