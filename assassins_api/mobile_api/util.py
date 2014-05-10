from django.http import HttpResponse
from django.template import Context, loader
from assassins_api import models

def return_html(page,data):
  # Load the template myblog/templates/index.html
  template = loader.get_template(page)
  context = Context(data)
  return HttpResponse(template.render(context))
  
  
#TODO raise 404  
def get_profile_given_user_id(user_id):
  profile = models.Profile.objects.filter(user=user_id).get();
  return profile;
  
def get_games_for_profile(profile):
  players = profile.players.all()
  games =[]
  for player in players:
    games.append(player.game)
  return games