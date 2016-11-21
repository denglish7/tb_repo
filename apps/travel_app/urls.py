from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^travels/$', views.index, name='index'),
    url(r'^logoff/$', views.logoff, name='logoff'),
    url(r'^destination/(?P<id>\d+)$', views.show, name='my_show'),
    url(r'^add_page/$', views.add_page, name='add_page'),
    url(r'^add_trip/$', views.add_trip, name='add_trip'),
    url(r'^join/(?P<id>\d+)$', views.join, name='my_join'),
]
