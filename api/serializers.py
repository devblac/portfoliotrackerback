from rest_framework import serializers
from api.models import Users, Transactions
from rest_framework.serializers import ModelSerializer

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id',
                  'user_name',
                  'password',
                  )

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