from django.conf.urls import patterns, include, url

from .views import busca

urlpatterns = patterns('',

    url(r'busca', busca),

)
