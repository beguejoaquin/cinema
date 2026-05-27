## Key info about Models

### Theater

The "type" field, which can be "regular" or "imax", affects the final price of
a movie ticket.
Is has a related field seats that groups all the Seats objects related to the
theater.
Joins Seats and Showtimes.

### Seat

The "type" field, which can be "regular" or "premium", and affects the final
price of a movie ticket.

### Showtime

Represents a showtime of a Movie in a certain Theater in a specific datetime.

### Reservation

Represents a reservation of a Seat for an specific Showtime.
Joins Showtimes and Seats.

### Movie ticket

Represents the ticket that the user pays and receives. It joins Reservations with
Orders

### Product

Consumables the user can buy when buying movie tickets.

### Order

The resume of the movie tickets and products the user buys.

## Processes

### Reservations and Seat availability

The seat availability for a requested showtime is defined by checking if there
is a "valid" or "pending" Reservation assigned to the seat in that particular showtime.

The reservation process works as follows:

1. The user select the seats that wants to book.
2. This seats are locked for 5 minutes by creating a Reservation with a "pending" state and an expiration timestamp for each seat.
3. If the booking is completed within those 5 minutes, the Reservation is marked as valid and the seats are now permanently blocked for the requested showtime.
4. If the 5 minutes pass, the expiration timestamp automatically marks the reservation as "expired" and filters the reservation at query time.
