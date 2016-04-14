from django.conf.urls import  include, url
from django.contrib import admin
from django.conf import settings
from monitor.views import *

urlpatterns = [
  url(r'^monitor/(?P<m>\d+)/$',monitor_view),
  url(r'^monitor/$',monitor),
  url(r'^monitor_graph/$',monitor_graph),
  url(r'^monitor_cpu_graph/(?P<c_type>\w{4}_\d+)/$',monitor_cpu_graph),
  url(r'^monitor_zabbix/$',monitor_zabbix),
  url(r'^alarm/$',alarm),
]
