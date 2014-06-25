from django.conf.urls import patterns, url

from sudocool import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^solve/$', views.solve, name = 'solve'),
    url(r'^solution/(\d+)$', views.solution, name = 'solution')
)
