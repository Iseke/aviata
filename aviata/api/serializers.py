from rest_framework import serializers


class FindeFlightSerializer(serializers.Serializer):
    fly_to = serializers.CharField(required=True)
    fly_from = serializers.CharField(required=True)
    fly_date = serializers.DateField(required=True)


class CheckTicketSerializer(serializers.Serializer):
    booking_token = serializers.CharField(required=True)
    pnum = serializers.IntegerField(required=True)
    bnum = serializers.IntegerField(required=True)