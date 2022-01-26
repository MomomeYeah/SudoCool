from django.urls import include, re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^sudocool/', include('sudocool.urls', namespace='sudocool')),
    re_path(r'^', include('sudocool.urls', namespace='sudocool')),
]
