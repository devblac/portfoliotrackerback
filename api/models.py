from enum import unique
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

    # python3 manage.py makemigrations
    # para crear la tabla y agregarla al panel administrador

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):
        
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")

        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser= True
        user.save(using=self._db)
        return 

class Users(AbstractBaseUser):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # login data
    class Meta: 
        db_table = 'Users'
    
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    def __str__(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
         return True

    def has_module_perms(self, app_label):
        return True

class Transactions(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    transacted_at = models.DateTimeField(auto_now_add=True, editable=False)
    symbol = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    transaction_type = models.CharField(max_length=50)
    class Meta: 
        db_table = 'Transactions'
