from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sudocool/', include('sudocool.urls', namespace = 'sudocool')),
    url(r'^$', include('sudocool.urls', namespace = 'sudocool')),
)
