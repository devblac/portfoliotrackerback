from rest_framework import serializers
from api.models import Users, Transactions
#from rest_framework.serializers import ModelSerializer
from django.conf import settings
from django.contrib.auth import get_user_model

class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("user_name", "email", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            user_name=self.validated_data["user_name"],
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("user_name", "password", "email")

class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transactions
        fields = [
            'transaction_id',
            'user_id',
            'symbol',
            'amount',
            'type',
            'transacted_at'
            ]