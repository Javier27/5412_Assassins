from django.conf.urls import patterns, include, url
from assassins_api.controllers import *
from assassins_api.controllers import admin_panel_controller

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/status/(?P<pk>[0-9]+)/$', game_controller.Status.as_view()),
    url(r'^game/start/(?P<pk>[0-9]+)/$', game_controller.Start.as_view()),
    url(r'^game/create/$', game_controller.Create.as_view()),
    url(r'^game/all/$', game_controller.List_All_Playing.as_view()),
    url(r'^login/$', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^users/status/(?P<pk>[0-9]+)/$', profile_controller.Status.as_view()),
    url(r'^users/delete/$', profile_controller.Delete().as_view()),
    url(r'^users/status/$', profile_controller.Self_Status.as_view()),
    url(r'^users/register/$', profile_controller.Create.as_view()),
    url(r'^users/find/$',profile_controller.Find.as_view()),
    url(r'^users/friend/$',profile_controller.Friend.as_view()),
    url(r'^users/unfriend/$',profile_controller.Friend.as_view()),
    url(r'^users/friends_list/(?P<pk>[0-9]+)/$', profile_controller.Friends_List.as_view()),
    url(r'^users/upload_picture/$', profile_controller.Upload_Picture.as_view()),
      
    url(r'^player/status/(?P<pk>[0-9]+)/$',player_controller.Status().as_view()),
    url(r'player/create/$', player_controller.Status().as_view()),
    url(r'player/attack/(?P<pk>[0-9]+)/$', player_controller.Status().as_view()),
    url(r'^admin_panel/$', admin_panel_controller.List_Games().as_view()),
)


urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)

