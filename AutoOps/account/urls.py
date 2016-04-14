from django.conf.urls import include, url
from django.contrib import admin
from account import views

urlpatterns = [
    url(r'^login/$',views.login_user,name='login'),
    url(r'^logout/$',views.logout_user,name='logout'),
    url(r'^account_list/$',views.account_list,name='logout'),
    url(r'^account_add/$',views.account_add),
    url(r'^account_del/(\d+)$',views.account_del),
    url(r'^account_edit/(\d+)$',views.account_edit),
    url(r'^account_detail/(\d+)$',views.account_detail),
    url(r'^logging/$',views.log_list),
    url(r'^setpasswd/(\d+)$',views.setpasswd),
    url(r'^dep_manage/$',views.dep_list),
]
