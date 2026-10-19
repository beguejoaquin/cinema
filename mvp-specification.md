# Cinema Minimum Viable Product (MVP) - Project Specifications

Cinema is a demo project that emulates a real-world fully functional cinema's website.

---

This document outlines the requirements, architecture, user flows, and administrative systems for the Cinema Minimum Viable Product (MVP) based on the project mind map.

---

## 1. Main User Flow

The core user journey focuses on browsing movies, viewing details, selecting seats, and checking out.

- **Browse movies**
  - Search bar
  - Filter
- **See movie info**
  - Important info always visible (genre, duration, title, trailer)
  - Extra info tab (synopsis, director, cast)
  - Booking tab
- **Book seats**
  - Select cinema
  - Select day
  - Select showtime
  - Select seats
- **Buy extras (consumables)**
- **Checkout**
  - Lock seats for 5 minutes
  - Log in needed
  - Paying method needed
  - Confirm purchase
  - Get tickets

---

## 2. Key Systems

The business logic governing seat locking, reservation states, and scheduled programming.

### Seat Reservation

- Each seat is represented as a `Seat` object in the DB.
- `Seats` objects are associated with `Reservations` objects.
- Seats locked (for a specific showtime) are associated with a `Reservation` with "pending" state.
- If the purchase is completed within 5 minutes after the seats are locked, the `Reservation` status is marked as "valid".
- Seats with no reservations marked as "valid" or "pending" are considered available.

### Showtime Schedule

- Showtime duration is based on movie duration + 15 minutes.
- Create a schedule for specific days and cinemas.
- Organize schedule across multiple theaters and with multiple movies.
- Automatically assign the amount of showtimes per day for each movie based on a "demand rank".

---

## 3. Administration

The management and backend controls for roles, platform permissions, and internal operations tracking.

### Admin Roles

- **Admin**
  - Can perform CRUD operations on all models
  - Can create Staff users
- **Staff**
  - Can perform CRUD operations only in Movie, Showtime, Reservation, Product, and Order models

### Admin Panel

- Tabs for CRUD operations on models
- Showtime schedule tab
- **Operations tab (shows all operations made)**
  - Staff only see operations made by them
  - Admin can see all operations
  - Filter operations by type or model

---

## 4. DevOps & Architecture

The deployment infrastructure, programming frameworks, and automation tooling.

- Docker based
- Frontend based on NextJS and deployed on Vercel
- Backend based on Django and deployed on Railway
- CI/CD with Github Actions

---

## 5. Extra Pages

Additional frontend pages supporting account management and user history.

- User info page (personal info and payment info)
- User reservations page

---

## 6. Extras

Quality assurance and developer documentation requirements.

- Tests
- Documentation
