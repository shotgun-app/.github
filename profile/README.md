<div align="center">
  <!-- TODO -->
  <img src="../content/logo.svg" alt="Shotgun App logo" height="70" />
  <h1 align="center">Call shotgun. Share the ride.</h1>
</div>

Project for course Agile software project management at University of Gothenburg.

Shotgun App is a carpooling web app that connects drivers who have empty seats with passengers travelling along similar routes. Drivers publish the trips they are already making, and passengers book the free seats at a price set by the driver. With fewer half-empty cars on the road, we help reduce travel costs, traffic and CO₂ emissions.

Shotgun is built by Project Group 4 as a university project. We work in sprints and release a new version of the app every sprint.

<div align="center">
  <!-- TODO -->
  <img src="../content/demo.gif" alt="Shotgun App Demo" width="1000" />
</div>

## Features
- **Trip creation**: drivers publish the trip they are already making, with from and to location, departure time, number of seats, price and contact.
- **Trip search**: find trips filtered by departure location, destination location, date and time.
- **Registration and login**: create an account and log in to use the app.
- **Basic profile**: see who you are travelling with before you book a ride.
- **Seat booking**: passengers reserve a seat without needing the driver's confirmation.
- **Shared data**: users, trips and bookings are stored in a database and visible to all users.
- **My rides**: grid view of the rides you offer and the seats you booked.
- **Rides management**: add, edit or remove your offered rides.
- **Seat overview**: see the remaining seats and the current participants of a trip.
- **Booking cancellation**: cancel a booking you cannot attend, freeing the seat for others.
- **Driver/Passenger ratings**: passengers rate the driver after the ride with stars and a written review, while drivers also rate their passenger. The reviews show up on their profiles.
- **Password reset**: request a reset email and set a new password.
- **Active sessions**: see all your active sessions and log out of all devices.
- **Consistent design**: same color palette, fonts and user experience across all screens.
- **Gamification**: ranking of the most active drivers and passengers.
- **Achievements**: earn in app badges for using the app.
- **Environmental impact**: see number of rides shared, distance covered and estimated CO₂ savings.
- **Baggage info**: passengers tell the driver the number, size and type of their bags.

## Tech Stack
- **Frontend**: Vue.js (Pinia for state management), TypeScript, Tailwind CSS, Vite
- **Backend & Database**: Go, Gin, GORM, PostgreSQL
- **Testing**: Vitest, Playwright
