from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sudocool/', include('sudocool.urls', namespace = 'sudocool')),
    url(r'^', include('sudocool.urls', namespace = 'sudocool')),
]
