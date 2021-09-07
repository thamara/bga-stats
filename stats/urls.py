from django.conf.urls import url, re_path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user_stats$', views.user_stats_post, name='user_stats_post'),
    re_path(r'^user_stats/(?P<player_id>[\w-]+)/$', views.user_stats, name='user_stats'),
    re_path(r'^game_detail/(?P<player_id>[\w-]+)/(?P<game>[\w-]+)/$', views.game_detail, name='game_detail'),
    re_path(r'^table_detail/(?P<player_id>[\w-]+)/(?P<table>[\w-]+)/$', views.table_detail, name='table_detail')
]
