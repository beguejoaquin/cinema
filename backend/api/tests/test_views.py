from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from api import models, serializers


class ViewsTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()

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


class CinemaViewTestCase(ViewsTestCase):
    def test_cinema_view_get(self):
        # Test list
        cinemas = models.Cinema.objects.all()
        data = serializers.CinemaSerializer(cinemas, many=True).data
        response = self.client.get("/api/cinemas/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

        # Test retrieve
        data = data[0]
        response = self.client.get(f"/api/cinemas/{data['id']}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

        # Test not found
        response = self.client.get("/api/cinemas/999999/")
        self.assertEqual(response.status_code, 404)

    def test_cinema_view_post(self):
        cinema_data = {
            "name": "South Cinema",
            "abbreviation": "STH",
            "location": "150th South Av",
            "imax": False,
        }
        response = self.client.post("/api/cinemas/", cinema_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], cinema_data["name"])
        self.assertEqual(response.data["abbreviation"], cinema_data["abbreviation"])
        self.assertEqual(response.data["location"], cinema_data["location"])
        self.assertEqual(response.data["imax"], cinema_data["imax"])

    def test_cinema_view_put(self):
        cinema = models.Cinema.objects.first()
        updated_data = {
            "name": "Updated Cinema",
            "abbreviation": "UPD",
            "location": "New Location",
            "imax": True,
        }
        response = self.client.put(f"/api/cinemas/{cinema.id}/", updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], updated_data["name"])
        self.assertEqual(response.data["imax"], updated_data["imax"])

    def test_cinema_view_patch(self):
        cinema = models.Cinema.objects.first()
        response = self.client.patch(f"/api/cinemas/{cinema.id}/", {"imax": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["imax"], True)

    def test_cinema_view_delete(self):
        cinema = models.Cinema.objects.first()
        response = self.client.delete(f"/api/cinemas/{cinema.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(models.Cinema.objects.filter(id=cinema.id).exists())


class TheaterViewTestCase(ViewsTestCase):
    def test_theater_view_get(self):
        theaters = models.Theater.objects.all()
        data = serializers.TheaterSerializer(theaters, many=True).data
        response = self.client.get("/api/theaters/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

        theater = theaters.first()
        response = self.client.get(f"/api/theaters/{theater.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(theater.id))

    def test_theater_view_post(self):
        cinema = models.Cinema.objects.first()
        theater_data = {
            "type": "R",
            "cinema": str(cinema.id),
            "number": 2,
            "rows": "A-B-C",
            "number_of_seats": 50,
        }
        response = self.client.post("/api/theaters/", theater_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["number"], 2)
        self.assertEqual(response.data["number_of_seats"], 50)

    def test_theater_view_put(self):
        theater = models.Theater.objects.first()
        updated_data = {
            "type": "I",
            "cinema": str(theater.cinema.id),
            "number": 10,
            "rows": "A-B-C-D",
            "number_of_seats": 100,
        }
        response = self.client.put(f"/api/theaters/{theater.id}/", updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["number_of_seats"], 100)

    def test_theater_view_patch(self):
        theater = models.Theater.objects.first()
        response = self.client.patch(
            f"/api/theaters/{theater.id}/", {"number_of_seats": 80}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["number_of_seats"], 80)

    def test_theater_view_delete(self):
        theater = models.Theater.objects.first()
        theater_id = theater.id
        response = self.client.delete(f"/api/theaters/{theater_id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(models.Theater.objects.filter(id=theater_id).exists())


# TODO: Make tests for Seat view

# TODO: Make tests for MovieGenre view

# TODO: Make tests for Movie view

# TODO: Make tests for MovieTicket view

# TODO: Make tests for Showtime view

# TODO: Make tests for Reservation view

# TODO: Make tests for Product view

# TODO: Make tests for Order view
