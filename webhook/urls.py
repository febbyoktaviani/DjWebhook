from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.handle_github_hook, name='index'),
]
    
