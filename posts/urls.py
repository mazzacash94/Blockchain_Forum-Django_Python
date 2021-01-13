from . import views
from django.urls import path


urlpatterns = [

    path('', views.home, name='homepage'),
    path('forum', views.forum, name='forum'),
    path('new', views.newPost, name='new post'),
    path('search', views.stringSearch, name='search'),
    path('last', views.lastHour, name='last hour posts'),

]