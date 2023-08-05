from django.urls import path

from . import views


app_name = 'trosnoth'
urlpatterns = [
    path('', views.index, name='index'),
    path('u/', views.userList, name='userlist'),
    path('u/<int:userId>/', views.userProfile, name='profile'),
    path(
        'u/<int:userId>/<str:nick>/', views.userProfile, name='profile'),
    path('g/', views.gameList, name='gamelist'),
    path('g/<int:gameId>/', views.viewGame, name='viewgame'),
    path('t/<int:tournamentId>/', views.tournament, name='tournament'),
    path('a/<int:arenaId>/', views.arena, name='arena'),

    path('ajax/pausearena', views.pauseArena, name='pausearena'),
    path('ajax/resumearena', views.resumeArena, name='resumearena'),
    path('ajax/restartarena', views.restartArena, name='restartarena'),
    path('ajax/resetarena', views.resetArena, name='resetarena'),
    path('ajax/disablearena', views.disableArena, name='disablearena'),
    path('ajax/enablearena', views.enableArena, name='enablearena'),
    path('ajax/disableshots', views.disableShots, name='disableshots'),
    path('ajax/enableshots', views.enableShots, name='enableshots'),
    path('ajax/disablecaps', views.disableCaps, name='disablecaps'),
    path('ajax/enablecaps', views.enableCaps, name='enablecaps'),

    path('tokenauth', views.tokenAuth, name='tokenauth'),
]

