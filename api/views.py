import json
from itertools import groupby
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet

from api.models import Transactions, Users

from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from api import serializers, models



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
    breakpoint()
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


def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def loginView(request):
    print('asdasd')
    serializer = serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(email=email, password=password)

    if user is not None:
        tokens = get_user_tokens(user)
        res = response.Response()
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens["access_token"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh_token"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.data = tokens
        res["X-CSRFToken"] = csrf.get_token(request)
        return res
    raise rest_exceptions.AuthenticationFailed(
        "Email or Password is incorrect!")


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([])
def registerView(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    ##breakpoint()
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return response.Response("Registered!")
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")


@rest_decorators.api_view(['POST'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()

        res = response.Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"]=None
        
        return res
    except:
        raise rest_exceptions.ParseError("Invalid token")


class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')


class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)

@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def user(request):
    try:
        user = models.Users.objects.get(id=request.user.id)
    except models.Users.DoesNotExist:
        return response.Response(status_code=404)

    serializer = serializers.UsersSerializer(user)
    return response.Response(serializer.data)