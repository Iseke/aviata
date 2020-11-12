from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import never_cache

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import FindeFlightSerializer, CheckTicketSerializer
from api.utils import try_cache, take_min_price, check_flight, return_helper


class FindFlightView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FindeFlightSerializer

    def post(self, request, *args, **kwargs):
        searching_field = request.data['fly_from'] + '_' + request.data['fly_to']
        print(searching_field)
        data = ''
        if searching_field in cache:
            data = cache.get(searching_field)
        res = take_min_price(data, request.data['fly_date'])
        if res != '':
            return Response({'booking_token': res['booking_token'], 'price': res['price']},
                            status=status.HTTP_302_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CheckFlightView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CheckTicketSerializer

    def post(self, request, *args, **kwargs):
        res = check_flight(request.data)
        res = return_helper(res)
        return res


class ClearView(generics.ListAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        data = cache.clear()
        print('delete cache')
        return Response('Deleted')
