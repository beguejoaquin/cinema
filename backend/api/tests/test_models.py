from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from api import models


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        # Create cinema
        cinema = models.Cinema.objects.create(
            name="North Cinema",
            abbreviation="NRT",
            location="150th North Av",
            imax=False,
        )

        # Create theater
        theater = models.Theater.objects.create(
            type=models.TheaterType.REGULAR,
            cinema=cinema,
            number=1,
            number_of_seats=75,
        )
        theater.set_rows(["A", "B", "C", "D", "E"])
        theater.save()

        # Create movies
        movie1 = models.Movie.objects.create(title="The Matrix", duration=120)
        movie2 = models.Movie.objects.create(title="Inception", duration=120)

        # Create movie ticket
        movie_ticket = models.MovieTicket.objects.create(
            type=models.MovieTicketType.REGULAR,
            price=12,
        )

        # Create showtimes
        showtime1 = models.Showtime.objects.create(
            movie=movie1,
            cinema=cinema,
            theater=theater,
            start=timezone.now() + timedelta(days=1),
            capacity_left=theater.number_of_seats,
        )
        showtime2 = models.Showtime.objects.create(
            movie=movie2,
            cinema=cinema,
            theater=theater,
            start=timezone.now() + timedelta(days=2),
            capacity_left=theater.number_of_seats,
        )

        # Create seats
        seats = []
        for n in range(1, 6):
            seat = models.Seat.objects.create(
                cinema=cinema,
                theater=theater,
                row="A",
                number=n,
                type=models.SeatType.REGULAR,
            )
            seats.append(seat)

        # Create reservation
        user = User.objects.create_user(username="testuser", password="test123")
        models.Reservation.objects.create(
            owner=user,
            showtime=showtime1,
            seat=seats[0],
            status=models.ReservationStatus.VALID,
            movie_ticket=movie_ticket,
        )
        models.Reservation.objects.create(
            owner=user,
            showtime=showtime2,
            seat=seats[0],
            status=models.ReservationStatus.VALID,
            movie_ticket=movie_ticket,
        )

        return super().setUp()


class TheaterTestCase(ModelsTestCase):
    def test_theater_set_rows(self):
        theater = models.Theater.objects.get(type=models.TheaterType.REGULAR)
        self.assertEqual(theater.rows, "A-B-C-D-E")

    def test_theater_get_rows(self):
        theater = models.Theater.objects.get(type=models.TheaterType.REGULAR)
        self.assertEqual(theater.get_rows(), ["A", "B", "C", "D", "E"])

    def test_theater_get_rows_as_choices(self):
        theater = models.Theater.objects.get(type=models.TheaterType.REGULAR)
        self.assertEqual(
            theater.get_rows_as_choices(),
            {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E"},
        )


class SeatTestCase(ModelsTestCase):
    def test_seat_is_available(self):
        showtime = models.Showtime.objects.first()
        seat1 = models.Seat.objects.get(reservations__showtime=showtime)
        seat2 = models.Seat.objects.exclude(reservations__showtime=showtime)[0]
        self.assertEqual(seat1.is_available(showtime), False)
        self.assertEqual(seat2.is_available(showtime), True)


class ShowtimeTestCase(ModelsTestCase):
    def test_showtime_save(self):
        movie = models.Movie.objects.get(title="The Matrix")
        showtime = models.Showtime.objects.get(movie=movie)
        end = showtime.start + timedelta(minutes=movie.duration + 15)
        self.assertEqual(showtime.end, end)

    def test_showtime_get_available_seats(self):
        showtime = models.Showtime.objects.first()
        seats = models.Seat.objects.filter(theater=showtime.theater).exclude(
            reservations__showtime=showtime
        )
        self.assertEqual(
            list(showtime.get_available_seats().values_list("id", flat=True)),
            list(seats.values_list("id", flat=True)),
        )


class ShowtimeManagerTestCase(ModelsTestCase):
    def test_showtime_manager_get_queryset(self):
        showtime = models.Showtime.objects.first()
        showtime.capacity_left = 0
        showtime.save()

        # The showtime should be marked as full.
        showtime.refresh_from_db()
        self.assertEqual(showtime.status, models.ShowtimeStatus.FULL)

        # The showtime should be marked as expired after 10 minutes.
        showtime.start = timezone.now() - timedelta(minutes=11)
        showtime.save()
        showtime.refresh_from_db()
        self.assertEqual(showtime.status, models.ShowtimeStatus.EXPIRED)


class ReservationTestCase(ModelsTestCase):
    def test_reservation_save(self):
        reservation = models.Reservation.objects.first()
        seat_code = reservation.seat.get_code()
        cinema = reservation.seat.cinema.abbreviation
        date = reservation.showtime.start.strftime("%y%m%d")
        count = models.Reservation.objects.filter(showtime=reservation.showtime).count()
        code = f"{seat_code}-{cinema}-{date}-{str(count).zfill(2)}"
        self.assertEqual(reservation.code, code)

        expiration = reservation.showtime.start + timedelta(minutes=30)
        self.assertEqual(reservation.expires_at, expiration)


class ReservationManagerTestCase(ModelsTestCase): ...
