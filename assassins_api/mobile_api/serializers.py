from rest_framework import serializers
from mobile_api.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id','username','email')
    
class GameSerializer(serializers.ModelSerializer):
  players = serializers.PrimaryKeyRelatedField(many=True)
  class Meta:
    model = Game
    fields = ('name', 'owner', 'status', 'id')
    
class PlayerSerializer(serializers.ModelSerializer):
  target = serializers.PrimaryKeyRelatedField(many=False, required=False)
  
  class Meta:
    model = Player
    fields = ('alive','game','target','profile','accepted','id')
    
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
  def validate_username(self, attrs, source):
          """
          check username doesnt contain @.
          """
          value = attrs[source]
          if "@" in value.lower():
              raise serializers.ValidationError("Username cannot contain @")
          return attrs
  
  class Meta:
    model = Profile
    fields = ('id','friends','players','owned_games','user','username','email','picture')

class FriendSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('username','email','id','picture')