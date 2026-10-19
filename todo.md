# Cinema MVP Todo List

## Project Overview
A cinema ticket booking system with Django backend and Next.js frontend. Docker-based with CI/CD.

---

## Phase 1: Core Booking Flow (MVP)

### 1.1 Backend - Core Models & API
- [ ] Review and finalize all models (Movie, Genre, Showtime, Theater, Cinema, Seat, Reservation, Order, Product, MovieTicket)
- [ ] Complete ShowtimeViewSet filtering (by movie, cinema, date, theater type)
- [ ] Implement seat availability logic (`Seat.is_available(showtime)`)
- [ ] Implement reservation seat locking (5-minute hold with PENDING → VALID transition)
- [ ] Auto-expire pending reservations after timeout
- [ ] Prevent double-booking of seats
- [ ] Create management command: `create_sample_data` (cinemas, theaters, seats, movies, showtimes, products)

### 1.2 Frontend - Movie Browsing
- [ ] Home page: fetch movies from `/movies/`
- [ ] Genre filtering (query param: `/movies/?genres=Action,Drama`)
- [ ] Search functionality
- [ ] Movie cards with hover effects, posters, duration, synopsis
- [ ] Movie detail page (`/movie/[id]/`): full info + available cinemas

### 1.3 Frontend - Showtime & Seat Selection
- [ ] Showtime listing: `/showtimes/?movie={id}` with date/cinema/type filters
- [ ] Theater selection per cinema (regular/IMAX)
- [ ] Seat map component: 10×20 grid, color-coded (available/selected/reserved/premium)
- [ ] Multiple seat selection with running price total
- [ ] Premium seat surcharge display

### 1.4 Frontend - Reservation & Checkout
- [ ] Create reservation: POST `/reservations/` with 5-minute countdown timer
- [ ] Handle reservation conflicts (seat already taken)
- [ ] Confirm reservation: transition PENDING → VALID
- [ ] Checkout: Create order via POST `/orders/` linking reservations and products
- [ ] Order summary with reservation codes and total breakdown

### 1.5 Frontend - Products & Cart
- [ ] Products page: fetch from `/products/` with "Add to Cart"
- [ ] Cart state management with localStorage persistence
- [ ] Cart icon with item count badge

---

## Phase 2: User Accounts

### 2.1 Authentication
- [ ] Login/Register pages
- [ ] JWT or session-based auth integration
- [ ] Protect order creation for authenticated users
- [ ] Link orders/reservations to user

### 2.2 User Pages
- [ ] User info page (personal info)
- [ ] User order history page (`/orders/`)
- [ ] User reservations page

---

## Phase 3: Admin Interface

### 3.1 Django Admin
- [ ] Configure admin for all models
- [ ] Inline reservations for showtimes
- [ ] Inline orders for users
- [ ] Custom admin actions for expiring reservations

### 3.2 Admin Roles
- [ ] Admin: CRUD all models, create Staff
- [ ] Staff: CRUD Movie, Showtime, Reservation, Product, Order only
- [ ] Operations log tab (Admin sees all, Staff sees own)

---

## Phase 4: Infrastructure & DevOps

### 4.1 Docker
- [ ] `docker-compose.yml` for local development
- [ ] Production Dockerfile for backend
- [ ] Production Dockerfile for frontend
- [ ] Environment variable configuration

### 4.2 CI/CD
- [ ] GitHub Actions for testing
- [ ] Auto-deploy on merge

---

## Phase 5: Polish & UX

### 5.1 UI/UX
- [ ] Loading states and spinners
- [ ] Error states with helpful messages
- [ ] Empty states
- [ ] Toast notifications
- [ ] Modal dialogs for confirmations
- [ ] Responsive design
- [ ] Smooth transitions/animations

### 5.2 Performance
- [ ] Next.js Image optimization
- [ ] Lazy loading components
- [ ] API response caching
- [ ] Pagination for list endpoints
- [ ] Database indexes for frequent queries

---

## Phase 6: Testing & Documentation

### 6.1 Backend Tests
- [ ] Model tests (seat availability, reservation expiration)
- [ ] ViewSet tests (API endpoints, filtering, permissions)
- [ ] Integration tests (reservation flow, order creation)

### 6.2 Frontend Tests
- [ ] Component unit tests
- [ ] User flow integration tests (browse → select → reserve → order)

### 6.3 Documentation
- [ ] README with setup instructions
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Architecture overview

---

## Priority Order Summary

1. **Week 1**: Backend core (models, seat locking, reservation flow) + sample data command
2. **Week 2**: Frontend core (movie browsing, showtime selection, seat map, reservation)
3. **Week 3**: Products, cart, checkout, order summary
4. **Week 4**: User auth, user pages, admin interface
5. **Week 5**: Docker, CI/CD, testing
6. **Week 6**: UI polish, performance, documentation