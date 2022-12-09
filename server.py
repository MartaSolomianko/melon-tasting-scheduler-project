"""Server for melon tasting appointment app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db, User, Reservation
from jinja2 import StrictUndefined
from datetime import datetime, time
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    username = session.get("username")

    # once logged in, you stay logged in
    if username:
        return redirect("/searchpage")
    
    return render_template("homepage.html")



@app.route("/login", methods=["POST"])
def login():
    """Process user Login."""

    username = request.form.get("username")

    # query db for username
    user = User.get_by_id(username)

    # if no username flash that user does not exist
    if not user:
        flash("no such user exists!")
        return redirect("/")
        
    else:
        # store that user's username in session and welcome them back
        session["username"] = user.username
        flash(f"Welcome back, {user.username}")

        return redirect("/searchpage")



@app.route("/searchpage/logout")
def user_logout():
    """Process user logout."""

    session.clear()

    return redirect("/")
    


@app.route("/searchpage")
def searchpage():
    """Display a form to search for reservations."""

    session_username = session.get("username")

    if session_username:
        return render_template("searchpage.html")
    


@app.route("/searchpage/search_results", methods=["POST"])
def show_search_results():
    """Display available reservations."""

    # grabs inputs from search page
    date = request.form.get("appt-date")
    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")
    # grabs username from session
    username = session.get("username")

    # format date to datetime object for db query
    date = datetime.strptime(date, "%Y-%m-%d").date()

    # query db for all appointments from that day
    check_available = Reservation.get_reservation_by_date(date)

    # this set will hold all times that are already reserved by other users 
    # for the day the current user requested to reserve a reservation on
    reserved_times = set()

    if check_available:
        # checks if there are no appointments made by that user on that same day
        for reservation in check_available:
            if reservation.username == username:
                flash("Sorry, you already booked an appointment on that day! Try a different date.")
                return redirect("/searchpage")
            # if there are no reservations made by the user, but there are reservations made on that day
            # add the start times of those reservations to reserved_times set
            else: 
                reserved_times.add(reservation.start_time)
                
    # if there are no reservations booked on that day by that user 
    # look for time availability
    # based on what is available (meaning check that that start time is not in the reserved_times set) 
    # returns available appointments within searched range for that day in 30 min increments
    # I think this will be a string response from the html form input
    # maybe will need to split string into hour and min
                
    requested_times = []

    # print()
    # print("this is the start time on line 114")
    # print(start_time)
    # print(type(start_time))

    start_time_hour = start_time[:2]
    start_time_min = start_time[-2:]
    # print(start_time_hour)
    # print(start_time_min)

    if start_time_min == "00" or start_time_min == "30":
        # change start_time to datetime time object 
        start_time = datetime.strptime(start_time, "%H:%M").time()
        # print()
        # print("this is the start_time after it becomes a time object.")
        # print(start_time)
        requested_times.append(start_time)

    else:
        # convert strings to int
        start_time_hour = int(start_time_hour)
        start_time_min = int(start_time_min)

        if start_time_min > 0 and start_time_min < 30:
            start_time_min = 30
            start_time = time(start_time_hour,start_time_min)

        elif start_time_min > 30 and start_time_min < 60:
            if start_time_hour == 23:
                start_time_hour = 00

            else: 
                start_time_hour += 1
            
            start_time_min = 00
            start_time = time(start_time_hour, start_time_min)

        if start_time not in reserved_times:
            requested_times.append(start_time)

    print()
    print("this is the start_time on line 152.")
    print(start_time)

    print()
    print("this is the requested times list")
    print(requested_times)

    print()
    print("this is the end time")
    print(end_time)
    print(type(end_time))

    # convert end_time to a time object 
    end_time = datetime.strptime(end_time, "%H:%M").time()

    print()
    print("this is the end time after it becomes a time object")
    print(end_time)
    print(type(end_time))

    print()
    print("these are the start hour and min")
    print(start_time_hour)
    print(type(start_time_hour))
    print(start_time_min)
    print(type(start_time_min))
    
    start_time_hour = int(start_time_hour)
    start_time_min = int(start_time_min)


    while start_time < end_time:

        if start_time_min == 0:
            start_time_min += 30

        else:
            if start_time_hour == 23:
                start_time_min = 0
                start_time_hour = 0

            else: 
                start_time_hour += 1
                start_time_min = 0

        start_time = time(start_time_hour, start_time_min)
        if start_time not in reserved_times:
            if start_time < end_time:
                requested_times.append(start_time)
        


    print()
    print("this is the requested times list after the while loop.")
    print(requested_times)


    # pass available appointments onto the search resutls page 
    return render_template("searchresults.html", requested_times=requested_times)
        


# route to book an appointment
@app.route("/book_reservation", methods=["POST"])
def submit_reservation():
    """Add a reservation to the db."""

    # recieve input from JS file
    # add it to db
    # commit to db
    # send a text response confirming that it was committed?
    # return jsonify

    pass



@app.route("/searchpage/my_reservations")
def show_reservations():
    """Display a user's reservations."""

    # grabs username from session
    username = session.get("username")

    # queries db for that user's reservations
    reservations = Reservation.get_reservations_by_username(username)

    # if there are no reservations for that user, have them stay on the search page
    if not reservations:
        flash("You don't have any reservations, yet!")
        return redirect("/searchpage")

    # otherwise, pass a list of reservations to the reservations page.
    return render_template("reservations.html", reservations=reservations)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)