from django.conf.urls import url, re_path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user_stats$', views.user_stats_post, name='user_stats_post'),
    re_path(r'^user_stats/(?P<player_id>[\w-]+)/$', views.user_stats, name='user_stats')
]
