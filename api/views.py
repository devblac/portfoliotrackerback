import json
from itertools import groupby
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from rest_framework.viewsets import ModelViewSet

from api.models import Transactions, Users
#from api.serializers import PostSerializer
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the portfolioTracker index.")

    #id=1
    #julian
    #blacher

def add_transaction(request: WSGIRequest): #user
    #breakpoint()
    print('hi')
    #request.GET 
    user = Users.objects.filter(id=1).first()
    if request.GET.get('symbol') and request.GET.get('amount') and request.GET.get('transaction_type'):  #
        symbol = request.GET.get('symbol');
        amount = request.GET.get('amount');
        transaction_type = request.GET.get('transaction_type');
        Transactions.objects.create(amount=amount, symbol=symbol, user_id=user, transaction_type=transaction_type)
    return JsonResponse({'message': 'The coins were added successfully'});
    # GET list of coins, POST a new coin, DELETE all coins

def get_coin_list(request):
    print('hi')
    return HttpResponse("Hi again");
    # GET list of coins, POST a new coin, DELETE all coins
 
def build_portfolio(txs: list[Transactions]) -> dict[str, int]:
    ## groupby require que estén ordenados por el campo que quiero ordenar
    grouped_txs = groupby(sorted(txs, key=lambda t: t.symbol), key=lambda t: t.symbol)
    return {symbol:sum([t.amount if t.transaction_type == 'buy' else -t.amount for t in ts]) for (symbol, ts) in grouped_txs}
     
#@api_view(['GET'])
def get_user_portfolio(request):
    ## print(Transactions.objects.filter(user_id=1).all())
    txs = Transactions.objects.filter(user_id=1).all()
    ##print(txs)
    result = build_portfolio(list(txs))
    print(type(result))
    print('julian', json.dumps(result))
    return JsonResponse(result);
    # GET user portfolio, // POST a new coin, DELETE all coins
 
#@api_view(['GET', 'PUT', 'DELETE'])
def get_coin(request, pk):
    # find coins by pk (id)
    HttpResponse("Hi again");
    try: 
        coin = Coins.objects.get(pk=pk) 
    except Coins.DoesNotExist: 
        return JsonResponse({'message': 'The coin does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE coin
    
    
#@api_view(['GET'])
def get_public_coins(request):
    # GET all published coins
    print('TODO get all published coins')
    return HttpResponse("Hi again");
