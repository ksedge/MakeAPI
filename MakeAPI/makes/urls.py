from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='makes_home'),
    url(r'^(?P<id>\w+(-\w+){4})$', views.resource, name='makes_resource'),
)
