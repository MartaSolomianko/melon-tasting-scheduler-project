# Melon Tasting Reservation Scheduler WIP
Task: Bulid an app that allows users to search for and book melon tasting reservations. The service will offer coverage 24/7/365 (including weekend and holidays).

## Features
### Login/Logout
* Users can Login to the app with a username
* Users can Logout

### Search for available reservations
* Users can choose a time range and date
* They can only reserve one tasting per day

### Search results
* Users are shown available reservations within their searched for range
* All reservations start on the hour or half hour

### View reservations
* Users can view all reservations they have booked

## Future Improvements
* Address edge-case in search results for when a user searches for a range that extends into a new day.

Flesh out scaffolding for: 
* Booking a reservation
* Editing a reservation
* Deleting a reservation

## Set Up
Clone or fork this repo: 
```
git clone https://github.com/MartaSolomianko/melon-tasting-scheduler-project.git
```
Create and activate a virtual environment inside your directory:
```
virtualenv env
source env/bin/activate
```
Install the dependencies:
```
pip install -r requirements.txt
```
Set up the database:
```
python3 seed_db.py
```
Run the app:
```
python3 server.py
```
Open up 'localhost:5000/' to access the app