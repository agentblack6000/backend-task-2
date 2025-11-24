# Metro Ticket Purchasing System

The system consists of the following 3 apps:

## Passengers

The passenger app takes care of the following:

### Login/Logout

Django's builtin User authentication takes care of the login/logout

### Sign Up

Uses Django's builtin features to sign up new Users and create a "Passenger" that can purchase tickets

### View Purchases

A 'dashboard' view displays all current tickets as well as links to other pages of the site.

### Add balance

Users need to add balance to their accounts before being able to purchase tickets.

### Purchase tickets

An implementation of Dijkstra's algorithm using Python's ```heapq``` library dynamically calculates the fare between 2 stations if possible

## Scanner Interface

The scanner app takes care of the following:

### Admin: Offline ticket creation

Admins can create tickets which are instantly marked as "in use"

### Scan incoming and outgoing passengers based on ticket ID

The ticket ID for each passenger is meant to be kept secret, passengers after login and entering the appropriate ticket ID (passenger must own the ticket) can update the status of their ticket

## Admin Interface

Superusers/admins can do the following:

### Add stations, lines, connections(tracks)

Add metro stations and lines, and tracks/connections between those stations (the start and end station, and the line it is part of, and other details like the travel time, distance, fare)

### Mark lines as operational/disabled

Can change the status of a particular metro line (active or disabled)

### Change the fare/travel time/distance for each track/connection between 2 stations

Update any of these fields through the admin interface.
