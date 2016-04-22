from django.conf.urls import  include, url
from django.contrib import admin
from django.conf import settings
from cmdb.views import *

urlpatterns = [
  url(r'^hardwareinfo/$',hardwareinfo),
  url(r'^assets_list/$',assets_list),
  url(r'^ip_list/$',ip_list),
  url(r'^ip_user/$',ip_user),
  url(r'^ipgroup_list/$',ipgroup_list),
  url(r'^multi_cmd/$',multi_cmd),
  #url(r'^multi_result/$',multi_result),
  url(r'^multi_info_collect/$',multi_info_collect),
  url(r'^multi_file/$',multi_file),
  url(r'^task_detail/(\d+)$',task_detail),
  url(r'^task_del/(\d+)$',task_del),
  url(r'^task_modify/(\d+)$',task_modify),
  url(r'^task_add/$',task_add),
  url(r'^manual/$',manual),
  
]
