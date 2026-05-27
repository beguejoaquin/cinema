from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from api import models, serializers


class CinemaViewset(viewsets.ModelViewSet):
    queryset = models.Cinema.objects.all()
    serializer_class = serializers.CinemaSerializer


class TheaterViewset(viewsets.ModelViewSet):
    queryset = models.Theater.objects.all()
    serializer_class = serializers.TheaterSerializer


class SeatViewset(viewsets.ModelViewSet):
    queryset = models.Seat.objects.all()
    serializer_class = serializers.SeatSerializer


class MovieGenreViewset(viewsets.ModelViewSet):
    queryset = models.MovieGenre.objects.all()
    serializer_class = serializers.MovieGenreSerializer


class MovieViewset(viewsets.ModelViewSet):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer

    def get_queryset(self):
        genres = self.request.query_params.get("genres")
        if genres:
            validated_genres = []
            for genre in genres.split(","):
                try:
                    validated_genres.append(models.MovieGenre.objects.get(name=genre))
                except models.MovieGenre.DoesNotExist as err:
                    raise NotFound(f"Error while querying gerne: {err}") from err
            return models.Movie.objects.filter(genres__in=validated_genres)

        return models.Movie.objects.all()


class MovieTicketViewset(viewsets.ModelViewSet):
    queryset = models.MovieTicket.objects.all()
    serializer_class = serializers.MovieTicketSerializer


class ShowtimeViewset(viewsets.ModelViewSet):
    queryset = models.Showtime.objects.all()
    serializer_class = serializers.ShowtimeSerializer


class ReservationViewset(viewsets.ModelViewSet):
    queryset = models.Reservation.objects.all()
    serializer_class = serializers.ReservationSerializer


class ProductViewset(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderViewset(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
