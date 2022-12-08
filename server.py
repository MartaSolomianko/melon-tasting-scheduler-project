"""Server for melon tasting appointment app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db, User, Reservation
from jinja2 import StrictUndefined
from datetime import datetime
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

    # query db for all appointments from that day
    check_available = Reservation.get_reservation_by_date(date)

    # checks if there are no appointments made by that user on that same day
    for reservation in check_available:
        if reservation.username == username:
            flash("Sorry, you already booked an appointment on that day! Try a different date.")
            return redirect("/searchpage")

        else:
            # returns available appointments within searched range for that day in 30 min increments

            # pass them onto the search resutls page 
            return render_template("searchresults.html")
        

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