from rest_framework import serializers

from api import models


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cinema
        fields = "__all__"


class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Theater
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seat
        fields = "__all__"


class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MovieGenre
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = "__all__"


class MovieTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MovieTicket
        fields = "__all__"


class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Showtime
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = "__all__"
