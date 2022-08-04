from django.urls import path #, url
#from django.conf.urls import urls

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('owned_coins', views.get_coin_list),
    path('(?P<pk>[0-9]+)$', views.get_coin),
    path('public_coins$', views.get_public_coins)
]