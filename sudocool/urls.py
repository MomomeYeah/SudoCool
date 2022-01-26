from django.urls import re_path

from sudocool import views


app_name = "sudocool"
urlpatterns = [
    re_path(r'^([0-9,]+)?$', views.index, name = 'index'),
    re_path(r'^solve/$', views.solve, name = 'solve'),
    re_path(r'^solution/(\d+)$', views.solution, name = 'solution'),
    re_path(r'^puzzle/', views.puzzle, name = 'puzzle'),
]
