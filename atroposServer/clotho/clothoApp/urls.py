from django.conf.urls import patterns, url
from clothoApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'createTelling', views.createTelling, name='createTelling'),
    url(r'getNextNode/(?P<telling_id>\d+)/(?P<player_id>[12])(/(?P<choice_id>\d))?', views.getNextNode, name='getNextNode'),
)