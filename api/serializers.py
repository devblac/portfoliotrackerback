from rest_framework import serializers
from api.models import User, Post
from rest_framework.serializers import ModelSerializer

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'user_name',
                  'mail',
                  'password'
                  'twitter',
                  'instagram')

class PostSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Post
        fields = ['id',
                  'title',
                  'content']
