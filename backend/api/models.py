import uuid
from datetime import timedelta, timezone

from django.contrib.auth.models import User
from django.db import models as m
from multiselectfield import MultiSelectField
from rest_framework.exceptions import APIException

REGULAR_SEAT_PRICE = 12
IMAX_SEAT_PRICE = 18
PREMIUM_SEAT_SURCHARGE = 6
THEATHER_PER_CINEMA = 10
ROWS_PER_THEATER = 10
SEATS_PER_ROW = 20


class Genre(m.TextChoices):
    ACTION = "ACT"
    ADVENTURE = "ADV"
    ANIMATION = "ANI"
    COMEDY = "COM"
    CRIME = "CRI"
    DOCUMENTARY = "DOC"
    DRAMA = "DRA"
    FAMILY = "FAM"
    FANTASY = "FAN"
    HORROR = "HOR"
    MYSTERY = "MYS"
    ROMANCE = "ROM"
    SCI_FI = "SCI"
    THRILLER = "THR"
    WAR = "WAR"
    WESTERN = "WES"


class Cinema(m.TextChoices):
    NORTH_CINEMA = "NC"
    SOUTH_CINEMA = "SC"
    WEST_CINEMA = "WC"
    EAST_CINEMA = "EC"


class TheaterType(m.TextChoices):
    REGULAR = "R"
    IMAX = "I"


class SeatType(m.TextChoices):
    REGULAR = "R"
    PREMIUM = "P"


class ReservationStatus(m.TextChoices):
    VALID = "V"
    PENDING = "P"
    EXPIRED = "E"


class ShowtimeStatus(m.TextChoices):
    AVAILABLE = "A"
    FULL = "F"
    EXPIRED = "E"


class MovieTicketType(m.TextChoices):
    REGULAR = "R"
    PREMIUM = "P"
    IMAX_REGULAR = "IR"
    IMAX_PREMIUM = "IP"


class OrderStatus(m.TextChoices):
    PAID = "P"
    CANCELED = "CA"
    COLLECTED = "CO"


class Movie(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = m.CharField(max_length=500)
    duration = m.IntegerField(verbose_name="duration in minutes")
    poster = m.ImageField(upload_to="uploads/movie_posters/", blank=True, null=True)
    trailer_url = m.CharField(max_length=1000)
    genres = MultiSelectField(choices=Genre, blank=True)
    synopsis = m.CharField(max_length=1000)
    director = m.CharField(max_length=255)
    cast = m.CharField(max_length=2500)
    imax = m.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Title: {self.title}; ID: {self.id}"


class MovieTicket(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = m.CharField(choices=MovieTicketType)
    price = m.DecimalField(max_digits=10, decimal_places=2)


class Theater(m.Model):
    """Create the Theater object, add the rows with the set_rows method and then
    save the object."""

    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = m.CharField(choices=TheaterType)
    cinema = m.CharField(choices=Cinema)
    rows = m.CharField(blank=True)
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


class Seat(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cinema = m.CharField(choices=Cinema)
    theater = m.ForeignKey(Theater, related_name="seats", on_delete=m.CASCADE)
    row = m.CharField(max_length=1)
    number = m.IntegerField()
    type = m.CharField()

    def __str__(self) -> str:
        return self.get_code()

    @property
    def is_available(self, showtime):
        for reservation in self.reservations.all():
            if reservation.showtime == showtime and reservation.status in [
                ReservationStatus.VALID,
                ReservationStatus.PENDING,
            ]:
                return False

        return True

    def get_code(self):
        return f"{(self.row)}{str(self.number).zfill(2)}-{str(self.theater).zfill(2)}"


class Showtime(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = m.ForeignKey(Movie, related_name="showtimes", on_delete=m.CASCADE)
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

    # TODO: Test this method.
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


class Reservation(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = m.ForeignKey(User, related_name="reservations", on_delete=m.CASCADE)
    showtime = m.ForeignKey(Showtime, related_name="reservations", on_delete=m.CASCADE)
    seat = m.ForeignKey(Seat, related_name="reservations", on_delete=m.DO_NOTHING)
    movie_ticket = m.ForeignKey(
        MovieTicket, related_name="reservations", on_delete=m.DO_NOTHING
    )
    status = m.CharField(choices=ReservationStatus)
    expires_at = m.DateTimeField()
    code = m.CharField(max_length=11, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.movie_ticket:
            try:
                movie_tickets = MovieTicket.objects.all()
                # Regular theater and seat
                if (
                    self.seat.theater.type == TheaterType.REGULAR
                    and self.seat.type == SeatType.REGULAR
                ):
                    self.movie_ticket = movie_tickets.get(type=MovieTicketType.REGULAR)
                # Regular theater and premium seat
                elif (
                    self.seat.theater.type == TheaterType.REGULAR
                    and self.seat.type == SeatType.PREMIUM
                ):
                    self.movie_ticket = movie_tickets.get(type=MovieTicketType.PREMIUM)
                # Imax theater and regular seat
                elif (
                    self.seat.theater.type == TheaterType.IMAX
                    and self.seat.type == SeatType.REGULAR
                ):
                    self.movie_ticket = movie_tickets.get(
                        type=MovieTicketType.IMAX_REGULAR
                    )
                # Imax theater and premium seat
                elif (
                    self.seat.theater.type == TheaterType.IMAX
                    and self.seat.type == SeatType.PREMIUM
                ):
                    self.movie_ticket = movie_tickets.get(
                        type=MovieTicketType.IMAX_PREMIUM
                    )
            except MovieTicket.DoesNotExist() as err:
                raise APIException("Movie ticket not found.") from err

        if not self.code:
            # Generate code format: SSS-TT-CC-YYMMDD-NN.
            # SSS = Seat, TT = Theater; CC = Cinema; YYMMDD = Year, Month, Day; NN = Sequential number
            seat_code = self.seat.get_code()
            cinema = self.seat.cinema()
            date = self.showtime.start.strftime("%y%m%d")
            count = Reservation.objects.filter(showtime=self.showtime).count() + 1

            self.code = f"{seat_code}-{cinema}-{date}-{str(count).zfill(2)}"

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
    name = m.CharField(max_length=200)
    description = m.TextField()
    thumbnail = m.ImageField(
        upload_to="uploads/product_thumbnails/", blank=True, null=True
    )
    price = m.DecimalField(max_digits=10, decimal_places=2)
    created_at = m.DateTimeField(auto_now_add=True)
    stock = m.IntegerField()

    def __str__(self):
        return self.name


# TODO: finish this model and define what models are pending.
class Order(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = m.ForeignKey(User, related_name="orders", on_delete=m.CASCADE)
    reservations = m.ManyToManyField(Reservation, related_name="order")
    products = m.ManyToManyField(Product, related_name="orders")
    total = m.DecimalField(max_digits=10, decimal_places=2)
    made_at = m.DateTimeField(auto_now_add=True)
    status = m.CharField(choices=OrderStatus)
