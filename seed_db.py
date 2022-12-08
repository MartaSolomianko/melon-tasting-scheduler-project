"""Script to drop and reseed database for melon tasting appointment app."""

import os
from datetime import time, date

import model
import server

os.system("dropdb melon_tastings_db")
os.system("createdb melon_tastings_db")

model.connect_to_db(server.app)
model.db.create_all()

# Create a fake user
username = "user01"
user = model.User.create(username)
model.db.session.add(user)
model.db.session.commit()

# Create a fake reservation
record_date = date(2022,12,10)
start_time = time(6,00)
end_time = time(6,30)
reservation = model.Reservation.create(user, record_date, start_time, end_time)
model.db.session.add(reservation)
model.db.session.commit()


