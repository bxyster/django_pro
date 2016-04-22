from django.conf.urls import  include, url
from django.contrib import admin
from django.conf import settings
from game.views import *

urlpatterns = [
  url(r'^game_list/$',game_list),
  url(r'^game_fun1/$',game_fun1),
]
