from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view

from rest_framework.viewsets import ModelViewSet

from api.models import Coins, Post
from api.serializers import PostSerializer
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the portfolioTracker index.")

class PostApiViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

#@api_view(['GET', 'POST', 'DELETE'])
def get_coin_list(request):
    print('hi')
    return HttpResponse("Hi again");
    # GET list of coins, POST a new coin, DELETE all coins
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def get_coin(request, pk):
    # find coins by pk (id)
    HttpResponse("Hi again");
    try: 
        coin = Coins.objects.get(pk=pk) 
    except Coins.DoesNotExist: 
        return JsonResponse({'message': 'The coin does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE coin
    
    
@api_view(['GET'])
def get_public_coins(request):
    # GET all published coins
    print('TODO get all published coins')
    return HttpResponse("Hi again");
