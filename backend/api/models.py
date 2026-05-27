import uuid
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models as m
from django.utils import timezone

REGULAR_SEAT_PRICE = 12
IMAX_SEAT_PRICE = 18
PREMIUM_SEAT_SURCHARGE = 6
THEATHER_PER_CINEMA = 10
ROWS_PER_THEATER = 10
SEATS_PER_ROW = 20


class Cinema(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=50, unique=True)
    abbreviation = m.CharField(max_length=3, unique=True)
    location = m.CharField(max_length=200, unique=True)
    imax = m.BooleanField()


class TheaterType(m.TextChoices):
    REGULAR = "R"
    IMAX = "I"


class Theater(m.Model):
    """Create the Theater object, add the rows with the set_rows method and then
    save the object."""

    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = m.CharField(choices=TheaterType, max_length=1)
    cinema = m.ForeignKey(Cinema, related_name="theaters", on_delete=m.CASCADE)
    number = m.IntegerField()
    rows = m.CharField(blank=True, max_length=100)
    number_of_seats = m.IntegerField()

    def get_rows(self):
        return self.rows.split("-")

    def get_rows_as_choices(self):
        choices = {}
        for row in self.get_rows():
            choices[row] = row
        return choices

    def set_rows(self, rows):
        self.rows = "-".join(rows)


class SeatType(m.TextChoices):
    REGULAR = "R"
    PREMIUM = "P"


class Seat(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cinema = m.ForeignKey(Cinema, related_name="seats", on_delete=m.CASCADE)
    theater = m.ForeignKey(Theater, related_name="seats", on_delete=m.CASCADE)
    row = m.CharField(max_length=1)
    number = m.IntegerField()
    type = m.CharField(choices=SeatType, max_length=1)

    def __str__(self) -> str:
        return self.get_code()

    def is_available(self, showtime):
        for reservation in self.reservations.all():
            if reservation.showtime == showtime and reservation.status in [
                ReservationStatus.VALID,
                ReservationStatus.PENDING,
            ]:
                return False

        return True

    def get_code(self):
        # Create a RNN-TT code (R = Row, NN = Number, TT, Theater)
        return f"{(self.row)}{str(self.number).zfill(2)}-{str(self.theater.number).zfill(2)}"


class MovieGenre(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=50, unique=True)


class Movie(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = m.CharField(max_length=500, unique=True)
    duration = m.IntegerField(verbose_name="duration in minutes")
    poster = m.ImageField(upload_to="uploads/movie_posters/", blank=True, null=True)
    trailer_url = m.CharField(max_length=1000)
    genres = m.ManyToManyField(MovieGenre, related_name="movies")
    synopsis = m.CharField(max_length=1000)
    director = m.CharField(max_length=255)
    cast = m.CharField(max_length=2500)
    imax = m.BooleanField(default=False)

    # TODO: Add "demand_rank" field for showtime schedule
    # TODO: Add "state" field with "new", "available" and "unlisted" options
    def __str__(self) -> str:
        return f"Title: {self.title}; ID: {self.id}"


class MovieTicketType(m.TextChoices):
    REGULAR = "R"
    PREMIUM = "P"
    IMAX_REGULAR = "IR"
    IMAX_PREMIUM = "IP"


class MovieTicket(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = m.CharField(choices=MovieTicketType, max_length=2)
    price = m.DecimalField(max_digits=10, decimal_places=2)


class ShowtimeStatus(m.TextChoices):
    AVAILABLE = "A"
    FULL = "F"
    EXPIRED = "E"


class Showtime(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = m.ForeignKey(Movie, related_name="showtimes", on_delete=m.CASCADE)
    cinema = m.ForeignKey(Cinema, related_name="showtimes", on_delete=m.CASCADE)
    theater = m.ForeignKey(Theater, related_name="showtimes", on_delete=m.CASCADE)
    start = m.DateTimeField()
    end = m.DateTimeField()
    capacity_left = m.IntegerField()
    status = m.CharField(default="available", max_length=10, choices=ShowtimeStatus)

    def save(self, *args, **kwargs):
        if self.start and self.movie:
            # Calculate end time: start time + movie duration + 15 minutes
            self.end = self.start + timedelta(minutes=self.movie.duration + 15)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.movie.title}; {self.theater.cinema} - {self.theater};  start={self.start}:{self.start.minute}; end={self.end.hour}:{self.end.minute}; ID: {self.id}"

    def get_available_seats(self):
        available_seats = self.theater.seats.exclude(reservations__showtime=self)
        return available_seats


class ShowtimeManager(m.Manager):
    def get_queryset(self):
        # Mark showtimes with available status and 0 capacity left as full.
        super().get_queryset().filter(
            status=ShowtimeStatus.AVAILABLE, capacity_left=0
        ).update(status=ShowtimeStatus.FULL)

        # Mark showtimes that have started 10 minutes ago as expired.
        now = timezone.now()
        super().get_queryset().filter(
            status__in=[ShowtimeStatus.AVAILABLE, ShowtimeStatus.FULL],
            start__lte=now - timedelta(minutes=10),
        ).update(status=ShowtimeStatus.EXPIRED)


class ReservationStatus(m.TextChoices):
    VALID = "V"
    PENDING = "P"
    EXPIRED = "E"


class Reservation(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = m.ForeignKey(User, related_name="reservations", on_delete=m.CASCADE)
    showtime = m.ForeignKey(Showtime, related_name="reservations", on_delete=m.CASCADE)
    seat = m.ForeignKey(Seat, related_name="reservations", on_delete=m.DO_NOTHING)
    movie_ticket = m.ForeignKey(
        MovieTicket, related_name="reservations", on_delete=m.DO_NOTHING
    )
    status = m.CharField(choices=ReservationStatus, max_length=1)
    expires_at = m.DateTimeField(blank=True)
    code = m.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate code format: SSS-TT-CCC-YYMMDD-NN.
            # SSS = Seat, TT = Theater; CCC = Cinema; YYMMDD = Year, Month, Day; NN = Sequential number
            seat_code = self.seat.get_code()
            cinema = self.seat.cinema.abbreviation
            date = self.showtime.start.strftime("%y%m%d")
            count = Reservation.objects.filter(showtime=self.showtime).count() + 1
            self.code = f"{seat_code}-{cinema}-{date}-{str(count).zfill(2)}"

        if not self.expires_at and self.showtime:
            self.expires_at = self.showtime.start + timedelta(minutes=30)
        elif not self.expires_at:
            raise ValueError("expires_at requires a valid showtime")

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Code: {self.code}; User: {self.user}; Showtime: {self.showtime.start}"


class ReservationManager(m.Manager):
    def get_queryset(self):

        now = timezone.now()
        super().get_queryset().filter(status="pending", expires_at__lt=now).update(
            status=ReservationStatus.EXPIRED
        )

        return super().get_queryset()


class Product(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = m.CharField(max_length=200, unique=True)
    description = m.TextField()
    thumbnail = m.ImageField(
        upload_to="uploads/product_thumbnails/", blank=True, null=True
    )
    price = m.DecimalField(max_digits=10, decimal_places=2)
    created_at = m.DateTimeField(auto_now_add=True)
    stock = m.IntegerField()

    def __str__(self):
        return self.name


class OrderStatus(m.TextChoices):
    PAID = "PA"
    CANCELED = "CA"
    COLLECTED = "CO"


class Order(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = m.ForeignKey(User, related_name="orders", on_delete=m.CASCADE)
    reservations = m.ManyToManyField(Reservation, related_name="order")
    products = m.ManyToManyField(Product, related_name="orders")
    total = m.DecimalField(max_digits=10, decimal_places=2)
    made_at = m.DateTimeField(auto_now_add=True)
    status = m.CharField(choices=OrderStatus, max_length=2)
