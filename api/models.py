from django.db import models

    # python3 manage.py makemigrations
    # para crear la tabla y agregarla al panel administrador

# Create your models here.
class Post(models.Model): 
    title = models.CharField(max_length=255),
    content = models.TextField()


class User(models.Model): 
    # login data
    user_name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    # Social Networks
    twitter = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    
class Portfolios(models.Model):
    portfolio_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

class TransactionTypes(models.Model):
    transaction_name = models.CharField(max_length=50)
    
class Coins(models.Model):
    coin_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    
class Transaction(models.Model):
    amount = models.IntegerField(default=0)
    settlement_date = models.DateTimeField('date published')
    id_portfolio = models.ForeignKey(Portfolios, on_delete=models.CASCADE)
    id_coin = models.ForeignKey(Coins, on_delete=models.CASCADE)
    id_transaction_type = models.ForeignKey(TransactionTypes, on_delete=models.CASCADE)