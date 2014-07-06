from django.conf.urls import patterns, url

from sudocool import views

urlpatterns = patterns('',
    url(r'^([0-9,]+)?$', views.index, name = 'index'),
    url(r'^solve/$', views.solve, name = 'solve'),
    url(r'^solution/(\d+)$', views.solution, name = 'solution'),
    url(r'^puzzle/', views.puzzle, name = 'puzzle'),
)
