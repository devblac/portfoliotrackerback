from django.urls import path #, url
#from django.conf.urls import urls

from . import views

app_name = "api"

urlpatterns = [
    path('', views.index, name='index'),
    path('owned_coins', views.get_coin_list), #OK
    path('public_coins', views.get_public_coins), #No funciona
    path('user_portfolio', views.get_user_portfolio), #OK
    path('add_transaction', views.add_transaction), #OK
    path('login', views.loginView),
    path('register', views.registerView),
    path('refresh-token', views.CookieTokenRefreshView.as_view()),
    path('logout', views.logoutView),
    path("user", views.user),
]