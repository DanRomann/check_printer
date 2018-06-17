from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^create_checks$', views.create_checks),
    url(r'^new_checks/$', views.new_checks),
    url(r'^check/$', views.check)
]