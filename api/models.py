from django.db import models

    # python3 manage.py makemigrations
    # para crear la tabla y agregarla al panel administrador

class Users(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    # login data
    class Meta: 
        db_table = 'Users'

class Transactions(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    transacted_at = models.DateTimeField(auto_now_add=True, editable=False)
    symbol = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    transaction_type = models.CharField(max_length=50)
    class Meta: 
        db_table = 'Transactions'
