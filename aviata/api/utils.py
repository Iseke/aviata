import requests

from django.core.cache import cache

from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response


def try_cache():
    url = 'https://api.skypicker.com/flights'
    directions = ['ALA_TSE', 'TSE_ALA', 'ALA_MOW', 'MOW_ALA', 'ALA_CIT',
                  'CIT_ALA', 'TSE_MOW', 'MOW_TSE', 'TSE_LED', 'LED_TSE']
    cur_date = datetime.now()
    dateTo = cur_date + timedelta(days=30)
    cur_date = cur_date.date().strftime('%d/%m/%Y')
    dateTo = dateTo.date().strftime('%d/%m/%Y')
    print(cur_date)
    print(dateTo)
    for direc in directions:
        data = {
            "fly_from": direc[:3],
            "fly_to": direc[4:],
            "dateFrom": cur_date,
            "dateTo": dateTo,
            "partner": "picky",
            "v": 3
        }
        res = requests.get(params=data, url=url)
        cur_data = res.json()['data']
        data = cache.set(direc, cur_data, 60*60*24)
        print(data)
    return 'ok'


def take_min_price(data, cur_date):
    minn = 10000000000
    chip_dir = ''
    for d in data:
        if datetime.utcfromtimestamp(int(d['dTimeUTC'])).strftime('%Y-%m-%d') == cur_date:
            if minn > d['price']:
                minn = d['price']
                chip_dir = d
    return chip_dir


def check_flight(data):
    url = 'https://booking-api.skypicker.com/api/v0.1/check_flights'
    request_data = {
        "v": 2,
        "booking_token": data['booking_token'],
        "pnum": data['pnum'],
        "bnum": data['bnum']
    }
    res = requests.get(params=request_data, url=url).json()
    res_data = {
        "flights_checked": res['flights_checked'],
        "flights_invalid": res['flights_invalid'],
        "price_change": res['price_change'],
        "total_price": res['total']
    }
    return res_data


def return_helper(res):
    if not res['flights_checked']:
        return Response({"status": 'Please try again after few seconds...'}, status=status.HTTP_404_NOT_FOUND)
    if not res['flights_invalid']:
        if not res['price_change']:
            return Response(
                {'status': "Everything is ok, you can book your ticket!", 'total_price': res['total_price']},
                status=status.HTTP_200_OK)
        return Response({'status': "Price of the ticket changed!!!", 'total_price': res['total_price']},
                        status=status.HTTP_302_FOUND)
    return Response({'status': 'Your flight is invalid, please choose another flight!'},
                    status=status.HTTP_404_NOT_FOUND)
