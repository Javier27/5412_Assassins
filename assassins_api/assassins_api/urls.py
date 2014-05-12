from django.conf.urls import patterns, include, url
from mobile_api.controllers import *
from mobile_api.controllers import admin_panel_controller
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/status/(?P<pk>[0-9]+)/$', game_controller.Status.as_view()),
    url(r'^game/start/(?P<pk>[0-9]+)/$', game_controller.Start.as_view()),
    url(r'^game/create/$', game_controller.Create.as_view()),
    url(r'^game/all/$', game_controller.List_All_Playing.as_view()),
    url(r'^game/owned/$',game_controller.List_All_Owned.as_view()),
    url(r'^game/check/assassination/$',game_controller.Check_Assassination.as_view()),
    url(r'^login/$', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^users/status/(?P<pk>[0-9]+)/$', profile_controller.Status.as_view()),
    url(r'^users/delete/$', profile_controller.Delete().as_view()),
    url(r'^users/status/$', profile_controller.Self_Status.as_view()),
    url(r'^users/register/$', profile_controller.Create.as_view()),
    url(r'^users/find/$',profile_controller.Find.as_view()),
    url(r'^users/friend/$',profile_controller.Friend.as_view()),
    url(r'^users/unfriend/$',profile_controller.Friend.as_view()),
    url(r'^users/friends_list/(?P<pk>[0-9]+)/$', profile_controller.Friends_List.as_view()),
    url(r'^users/from/player/(?P<pk>[0-9]+)/$', profile_controller.Profile_From_Player.as_view()),
    url(r'^users/upload_picture/$', profile_controller.Upload_Picture.as_view()),
    url(r'^users/pending_games/$', profile_controller.Pending_Requests.as_view()),
    url(r'^users/accept/(?P<pk>[0-9]+)/$$', profile_controller.Accept_Request.as_view()),
    url(r'^users/decline/(?P<pk>[0-9]+)/$$', profile_controller.Decline_Request.as_view()),
    url(r'^player/status/(?P<pk>[0-9]+)/$',player_controller.Status().as_view()),
    url(r'player/create/$', player_controller.Create().as_view()),
    url(r'player/create/multiple/$', player_controller.Create_Multiple().as_view()),
    url(r'player/attack/$', player_controller.Attack().as_view()),
    url(r'^admin_panel/$', admin_panel_controller.List_Games().as_view()),
    url(r'^admin_panel/create/game/$', admin_panel_controller.Create_Game().as_view()),
    url(r'^admin_panel/decline/(?P<game_id>[0-9]+)/$', admin_panel_controller.Decline_Game().as_view()),
    url(r'^admin_panel/accept/(?P<game_id>[0-9]+)/$', admin_panel_controller.Accept_Game().as_view()),
    url(r'^admin_panel/start/(?P<game_id>[0-9]+)/$', admin_panel_controller.Start_Game().as_view()),
    url(r'^admin_panel/friends/$', admin_panel_controller.Friends().as_view()),
    url(r'^admin_panel/stats/AOL/$', admin_panel_controller.Stats_AOL().as_view()),
    url(r'^admin_panel/stats/Assassinations/$', admin_panel_controller.Stats_Assassinations().as_view()),
    url(r'^admin_panel/stats/Attempts/$', admin_panel_controller.Stats_Attempts().as_view()),
)

urlpatterns += staticfiles_urlpatterns()


urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)

