from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"cinemas", views.CinemaViewset, basename="cinema")
router.register(r"theaters", views.TheaterViewset, basename="theater")
router.register(r"seats", views.SeatViewset, basename="seat")
router.register(r"movie-genres", views.MovieGenreViewset, basename="movie-genre")
router.register(r"movies", views.MovieViewset, basename="movie")
router.register(r"movie-tickets", views.MovieTicketViewset, basename="movie-ticket")
router.register(r"showtimes", views.ShowtimeViewset, basename="showtime")
router.register(r"reservations", views.ReservationViewset, basename="reservation")
router.register(r"orders", views.OrderViewset, basename="order")
router.register(r"products", views.ProductViewset, basename="product")


urlpatterns = [
    path("", include(router.urls)),
]
