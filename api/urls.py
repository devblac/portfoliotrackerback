from django.urls import path #, url
#from django.conf.urls import urls

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('owned_coins', views.get_coin_list), #OK
    path('public_coins', views.get_public_coins), #No funciona
    path('user_portfolio', views.get_user_portfolio), #OK
    path('add_transaction', views.add_transaction) #OK
]